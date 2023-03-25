from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from NewsPortal.models import PostCategory
from NewsPortal.tasks import new_post_notice_email


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        new_post_notice_email.delay(instance.id)

        # categories = instance.postCategory.all()
        # subscribers: list[str] = []
        # for category in categories:
        #     subscribers += category.subscribers.all()
        #
        # subscribers = [s.email for s in subscribers]
        # preview = instance.preview()
        # pk = instance.pk
        # title = instance.title
        #
        # html_content = render_to_string(
        #     'post_created_email.html',
        #     {
        #         'text': preview,
        #         'link': f'http://127.0.0.1:8000/news/{pk}'
        #     }
        # )
        #
        # for email in subscribers:
        #     new_post_notice_email.delay(email, title, html_content)


# def send_notifications(preview, pk, title, subscribers):
#     html_content = render_to_string(
#         'post_created_email.html',
#         {
#             'text': preview,
#             'link': f'http://127.0.0.1:8000/news/{pk}'
#         }
#     )
#
#     for email in subscribers:
#         msg = EmailMultiAlternatives(
#             subject=title,
#             body='',
#             from_email=None,
#             to=[email],
#         )
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()


# from django.contrib.auth.models import User
# from django.core.mail import EmailMultiAlternatives
# from django.db.models.signals import post_save
# from django.dispatch import receiver
#
# from .models import Post
#
#
# @receiver(post_save, sender=Post)
# def post_created(instance, created, **kwargs):
#     if not created:
#         return
#
#     emails = User.objects.filter(
#         subscriptions__category=instance.postCategory
#     ).values_list('email', flat=True)
#
#     subject = f'Новый пост в категории "{instance.postCategory}"'
#
#     text_content = (
#         f'Заголовок: {instance.title}\n'
#         f'Текст: {instance.text}\n\n'
#         f'Ссылка на пост: http://127.0.0.1:8000{instance.get_absolute_url()}'
#     )
#     html_content = (
#         f'Заголовок: {instance.title}<br>'
#         f'Текст: {instance.text}<br><br>'
#         f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
#         f'Ссылка на пост</a>'
#     )
#     for email in emails:
#         msg = EmailMultiAlternatives(subject, text_content, None, [email])
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()
