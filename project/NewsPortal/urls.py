from django.urls import path
from .views import *

from django.views.decorators.cache import cache_page

# Ссылки второго уровня
urlpatterns = [
    # path('', index),
    path('', Index.as_view(), name='index'),
    path('chat/', PostList.as_view()),
    path('contacts/', PostList.as_view()),
    path('about/', PostList.as_view()),

    path('news/', PostList.as_view(), name='post_list'),
    path('news/<int:pk>/',
         cache_page(1 * 1)(PostDetail.as_view()), name='post_detail'),
    path('news/search/', PostSearch.as_view(), name='post_search'),
    path('news/create/', PostCreate.as_view(), name='post_create'),
    path('news/<int:pk>/edit/', PostEdit.as_view(), name='post_edit'),
    path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

    path('articles/', PostList.as_view(), name='art_list'),
    path('articles/<int:pk>/', PostDetail.as_view(), name='art_detail'),
    path('articles/create/', PostCreate.as_view(), name='art_create'),
    path('articles/<int:pk>/edit/', PostEdit.as_view(), name='art_edit'),
    path('articles/<int:pk>/delete/', PostDelete.as_view(), name='art_delete'),

    path('upgrade/', upgrade_user, name='account_upgrade'),
    path('news/categories/<int:pk>/',
         CategoryListView.as_view(), name='category_list'),
    path('news/categories/<int:pk>/subscribe/', subscribe, name='subscribe'),
    path('subscriptions/', subscriptions, name='subscriptions'),
]
