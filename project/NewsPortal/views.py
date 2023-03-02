import datetime
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .filters import PostFilter
from .models import Post
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


class PostList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'news.html'
    context_object_name = 'news'
    paginate_by = 10


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


class PostCreate(CreateView):
    form_class = PostEditForm
    model = Post
    template_name = 'post_create.html'

    # def form_valid(self, form):
    #     post = form.save(commit=False)
    #     post.categoryType = 'Новость'
    #     return super().form_valid(form)


class PostEdit(UpdateView):
    form_class = PostEditForm
    model = Post
    template_name = 'post_edit.html'


class PostDelete(DeleteView):
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
