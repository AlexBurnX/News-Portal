import datetime
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from .filters import PostFilter
from .models import *
from .forms import *


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
    paginate_by = 8

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
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
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


class PostEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('NewsPortal.change_post',)
    form_class = PostEditForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('NewsPortal.delete_post',)
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')

# def post_create(request):
#     form = PostEditForm()
#
#     if request.method == 'POST':
#         form = PostEditForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect('/news/')
#
#     return render(request, 'post_create.html', {'form': form})
