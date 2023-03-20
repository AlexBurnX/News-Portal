import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin
)
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.models import Group

from .filters import PostFilter
from .models import *
from .forms import *


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
    category.subscribers.add(user)

    message = 'Вы успешно подписались на рассылку новостей категории'
    return render(request, 'subscribe.html',
                  {'category': category, 'message': message})


def index(request):
    posts = Post.objects.all()
    # Словарь для передачи данных в шаблон страницы
    context = {
        'posts': posts,
        'name': 'Microsoft',
        'title': 'Index'
    }
    return render(request, 'index.html', context=context)


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
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_author'] = self.request.user.groups.filter(
            name='authors').exists()
        return context


class PostDetail(DetailView):
    model = Post
    context_object_name = 'post'
    template_name = 'post.html'


class PostSearch(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'search.html'
    context_object_name = 'news'
    paginate_by = 7

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('NewsPortal.add_post',)
    # raise_exception = True
    form_class = PostEditForm
    model = Post
    template_name = 'post_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user.author
        return super().form_valid(form)

    # def form_valid(self, form):
    #     post = form.save(commit=False)
    #     post.categoryType = 'Новость'
    #     return super().form_valid(form)


class PostEdit(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('NewsPortal.change_post',)
    form_class = PostEditForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    permission_required = ('NewsPortal.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')


class CategoryListView(PostList):
    model = Post
    template_name = 'category_list.html'
    context_object_name = 'category_news_list'
    paginate_by = 8

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
