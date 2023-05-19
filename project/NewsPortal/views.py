from django.forms import model_to_dict
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import Group

from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from .serializers import *

from .filters import PostFilter
from .models import *
from .forms import *

from django.views.decorators.cache import cache_page
from django.core.cache import cache

from django.utils.translation import gettext as _
from django.utils.translation import activate, get_supported_language_variant
from django.utils import timezone
import pytz
import json

import logging

logger = logging.getLogger(__name__)


class Index(View):
    logger.info('INFO')

    def get(self, request):
        models = MyModel.objects.all()
        categories = Category.objects.all()
        posts = Post.objects.all()
        # Словарь для передачи данных в шаблон страницы
        context = {
            'title': _('Main'),
            'models': models,
            'categories': categories,
            'posts': posts[::-1],
            'name': 'Microsoft',
            'current_time': timezone.localtime(timezone.now()),
            'timezones': pytz.common_timezones
        }
        return HttpResponse(render(request, 'index.html', context=context))

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')


@cache_page(1 * 1)  # Хэширование на 1 сек
def index(request):
    logger.info('INFO')
    models = MyModel.objects.all()
    categories = Category.objects.all()
    posts = Post.objects.all()
    # Словарь для передачи данных в шаблон страницы
    context = {
        'models': models,
        'categories': categories,
        'posts': posts,
        'name': 'Microsoft',
        'title': _('Index'),
    }
    return render(request, 'index.html', context=context)


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        user = request.user
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscriber.objects.create(user=request.user, category=category)
            category.subscribers.add(user)
        elif action == 'unsubscribe':
            Subscriber.objects.filter(
                user=request.user,
                category=category,
            ).delete()
            category.subscribers.remove(user)

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscriber.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )


@login_required
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)

    if not category.subscribers.filter(id=user.id).exists():
        category.subscribers.add(user)
        message = 'Вы успешно подписались на рассылку новостей категории'
        return render(request, 'subscribe.html',
                      {'category': category, 'message': message})


@login_required
def upgrade_user(request):
    user = request.user
    group = Group.objects.get(name='authors')
    if not user.groups.filter(name='authors').exists():
        group.user_set.add(user)
        if not Author.objects.filter(authorUser=user).exists():
            Author.objects.create(authorUser=User.objects.get(pk=user.id))

    return redirect('/news/')


class PostList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 7

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Latest')
        context['is_author'] = self.request.user.groups.filter(
            name='authors').exists()
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        # return redirect('/news')
        return redirect(request.META.get('HTTP_REFERER'))


class PostDetail(DetailView):
    """
    Детальное представление поста
    """
    model = Post
    context_object_name = 'post'
    template_name = 'post.html'
    queryset = Post.objects.all()

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request, **kwargs):
        request.session['django_timezone'] = request.POST['timezone']
        # return redirect(f'/news/{self.kwargs["pk"]}')
        return redirect(request.META.get('HTTP_REFERER'))


class PostSearch(ListView):
    form_class = PostSearchForm
    model = Post
    ordering = '-dateCreation'
    template_name = 'search.html'
    context_object_name = 'news'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request, **kwargs):
        request.session['django_timezone'] = request.POST['timezone']
        # return redirect(f'/news/{self.kwargs["pk"]}')
        return redirect(request.META.get('HTTP_REFERER'))


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('NewsPortal.add_post',)
    # raise_exception = True
    form_class = PostEditForm
    model = Post
    template_name = 'post_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request, **kwargs):
        request.session['django_timezone'] = request.POST['timezone']
        # return redirect(f'/news/{self.kwargs["pk"]}')
        return redirect(request.META.get('HTTP_REFERER'))


class PostEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('NewsPortal.change_post',)
    form_class = PostEditForm
    model = Post
    template_name = 'post_edit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request, **kwargs):
        request.session['django_timezone'] = request.POST['timezone']
        # return redirect(f'/news/{self.kwargs["pk"]}')
        return redirect(request.META.get('HTTP_REFERER'))


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('NewsPortal.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_time'] = timezone.localtime(timezone.now())
        context['timezones'] = pytz.common_timezones
        return context

    def post(self, request, **kwargs):
        request.session['django_timezone'] = request.POST['timezone']
        # return redirect(f'/news/{self.kwargs["pk"]}')
        return redirect(request.META.get('HTTP_REFERER'))


class CategoryListView(PostList):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(
            postCategory=self.category).order_by('-dateCreation')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in \
                                       self.category.subscribers.all()
        context['category'] = self.category
        return context

    def post(self, request, **kwargs):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect(request.META.get('HTTP_REFERER'))


# ========================= API =========================

class NewsViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    queryset = Post.objects.filter(categoryType='NW')
    serializer_class = NewsSerializer

    @action(methods=['get'], detail=True)
    def category(self, request, pk=None):
        category = Category.objects.get(pk=pk)
        return Response({'category': category.name})


class ArticlesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    queryset = Post.objects.filter(categoryType='AR')
    serializer_class = ArticlesSerializer

    @action(methods=['get'], detail=True)
    def category(self, request, pk=None):
        category = Category.objects.get(pk=pk)
        return Response({'category': category.name})


class CategoriesViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
