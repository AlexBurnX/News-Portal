from .models import Post, Category, MyModel
from modeltranslation.translator import register, TranslationOptions


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('title', 'text',)


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(MyModel)
class MyModelTranslationOptions(TranslationOptions):
    fields = ('name',)
