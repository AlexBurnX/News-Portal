import time
import datetime
from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from NewsPortal.models import Post, Category


@shared_task
def new_post_notification_email(title, email, html_content):
    print(f'----------------------------------------')
    print(f'Письмо отправлено на "{email}"')
    print(f'----------------------------------------')
    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=None,
        to=[email],
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()


@shared_task
def weekly_news_mailer():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(dateCreation__gte=last_week)
    categories = set(posts.values_list('postCategory__name', flat=True))
    subscribers = set(Category.objects.filter(
        name__in=categories).values_list('subscribers__email', flat=True))

    html_content = render_to_string(
        'daily_post.html',
        {
            'link': f'http://127.0.0.1:8000/',
            'posts': posts,
        }
    )
    for email in subscribers:
        msg = EmailMultiAlternatives(
            subject='Статьи за неделю',
            body='',
            from_email=None,
            to=[email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        print(f'Email: {email}')
        print(html_content)


# @shared_task
# def hello():
#     time.sleep(10)
#     print('Hello, world!')
#
#
# @shared_task
# def printer(N):
#     for i in range(N):
#         time.sleep(1)
#         print(i + 1)
