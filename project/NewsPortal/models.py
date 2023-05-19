from django.db import models
from django.db.models import Sum
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime

from django.core.cache import cache
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy, pgettext_lazy


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=
                                                           Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()

    def __str__(self):
        return f'{self.authorUser}'

    class Meta:
        verbose_name = _('Author')
        verbose_name_plural = _('Authors')


class Post(models.Model):
    author = models.ForeignKey(Author,
                               verbose_name=pgettext_lazy('Author', 'Author'),
                               on_delete=models.CASCADE)

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS, gettext_lazy('News')),
        (ARTICLE, gettext_lazy('Article')),
    )
    categoryType = models.CharField(max_length=2,
                                    choices=CATEGORY_CHOICES,
                                    default=NEWS)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField('Category', through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    @property
    def likes(self):
        return self.rating

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[:124]}... '

    def __str__(self):
        # return f'{self.title.title()} :: {self.text[:40]}... '
        return f'{self.title.title()} '

    def get_absolute_url(self):
        # return reverse('post_detail', args=[str(self.id)])
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        cache.delete(f'post-{self.pk}')

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')


class Category(models.Model):
    name = models.CharField(max_length=64, unique=True,
                            verbose_name=pgettext_lazy(
                                'Name', 'Name'),
                            help_text=_('category name'))
    description = models.TextField(
        null=True, blank=True, verbose_name=_('Description'),
        help_text=_('there may be a more detailed description here')
    )
    subscribers = models.ManyToManyField(
        User, related_name='categories', blank=True,
        verbose_name='Subscribers',
        help_text=_('Hold down "CTRL" or "Command" on Mac, '
                    'to select more than one.')
    )

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['name']  # Сортировка

    def subscribe(self):
        pass

    def get_category(self):
        return f'{self.name}'

    def __str__(self):
        return f'{self.name}'


class PostCategory(models.Model):
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)
    categoryThrough = models.ForeignKey('Category', on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('Post Category')
        verbose_name_plural = _('Post Categories')

    def __str__(self):
        return f'{self.categoryThrough.name} | {self.postThrough.title}'


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')

    def __str__(self):
        dateCreation = f'{self.dateCreation:%d.%m.%Y}'
        return f'{self.commentUser} ({dateCreation}) :: {self.text}'


# Subscription
class Subscriber(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )


class MyModel(models.Model):
    name = models.CharField(max_length=100)
    kind = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='kinds',
        verbose_name=pgettext_lazy(_('help text for MyModel model'),
                                   _('This is the help text')),
    )

    class Meta:
        verbose_name = _('My Model')
        verbose_name_plural = _('My Models')
