from django.contrib import admin
from .models import *
from modeltranslation.admin import TranslationAdmin, TabbedTranslationAdmin


def reset_rating(modeladmin, request, queryset):
    reset_rating.short_description = 'Сбросить рейтинг'
    queryset.update(rating=0)


class PostCategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1


class PostAdmin(TabbedTranslationAdmin):
    model = Post
    list_display = ('title', 'id', 'author', 'likes')
    list_filter = ('rating', 'dateCreation')
    search_fields = ('title', 'postCategory__name')
    actions = [reset_rating]
    inlines = [PostCategoryInline]


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('authorUser', 'ratingAuthor')
    list_filter = ('authorUser', 'ratingAuthor')


class CategoryAdmin(TabbedTranslationAdmin):
    model = Category
    list_display = ('name',)
    list_filter = ('name', 'subscribers')
    inlines = [PostCategoryInline]


class CommentAdmin(admin.ModelAdmin):
    list_display = ('commentUser', 'dateCreation', 'text', 'commentPost')
    list_filter = ('commentUser', 'dateCreation')


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('postThrough', 'categoryThrough')
    list_filter = ('categoryThrough',)


class MyModelAdmin(TabbedTranslationAdmin):
    model = MyModel


admin.site.register(Author, AuthorAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(MyModel, MyModelAdmin)

# admin.site.unregister(Comment)
