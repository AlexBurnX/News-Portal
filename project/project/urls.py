from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from NewsPortal.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'news', NewsViewSet, basename='News')
router.register(r'articles', ArticlesViewSet, basename='Articles')
router.register(r'categories', CategoriesViewSet, basename='Categories')

# Ссылки первого уровня
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls, name='admin'),
    path('', include('NewsPortal.urls')),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/', include('accounts.urls')),
    path('accounts/', include('allauth.urls')),
    path('swagger-ui/', TemplateView.as_view(
        template_name='swagger-ui.html',
        extra_context={'schema_url': 'openapi-schema'}
    ), name='swagger-ui'),
    path('api/v1/', include(router.urls)),
]
