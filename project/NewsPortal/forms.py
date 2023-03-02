from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class PostEditForm(forms.ModelForm):
    # author = forms.CharField(label='Автор')
    # category = forms.ModelChoiceField(
    #     label='Категория', queryset=Category.objects.all(),
    # )
    # title = forms.CharField(label='Заголовок')
    # text = forms.IntegerField(label='Текст поста')

    class Meta:
        model = Post
        fields = [
            'author',
            'postCategory',
            'categoryType',
            'title',
            'text',
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        text = cleaned_data.get('text')
        if text is not None and len(text) < 10:
            raise ValidationError({
                'text': 'Новость не может быть менее 10 символов.'
            })
        if title[0].islower():
            raise ValidationError(
                'Заголовок должен начинаться с заглавной буквы.'
            )
        if text == title:
            raise ValidationError(
                'Текст новости не должен быть идентичным заголовку.'
            )

        return cleaned_data
