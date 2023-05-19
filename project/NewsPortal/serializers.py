from rest_framework import serializers
from .models import *


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'author', 'categoryType', 'dateCreation',
                  'postCategory', 'title', 'text', 'rating')


class ArticlesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'author', 'categoryType', 'dateCreation',
                  'postCategory', 'title', 'text', 'rating')


class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)
