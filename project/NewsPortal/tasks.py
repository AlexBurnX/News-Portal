import time
import datetime
from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from NewsPortal.models import Post, Category


@shared_task
def new_post_notice_email(instance_id):
    instance = Post.objects.get(pk=instance_id)
    categories = instance.postCategory.all()
    subscribers: list[str] = []
    for category in categories:
        subscribers += category.subscribers.all()

    subscribers = list(set([s.email for s in subscribers]))
    preview = instance.preview()
    pk = instance.pk
    title = instance.title

    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'http://127.0.0.1:8000/news/{pk}'
        }
    )

    for email in subscribers:
        send_emails.delay(email, title, html_content)


@shared_task
def send_emails(email, title, html_content):
    time.sleep(3)
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
