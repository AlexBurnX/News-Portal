from django.contrib import admin
from django.urls import path, include


# Ссылки первого уровня
urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', include('NewsPortal.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    # path('chat/', include('NewsPortal.urls')),
    # path('contacts/', include('NewsPortal.urls')),
    # path('about/', include('NewsPortal.urls')),
    # path('news/', include('NewsPortal.urls')),
    # path('articles/', include('NewsPortal.urls')),
]
