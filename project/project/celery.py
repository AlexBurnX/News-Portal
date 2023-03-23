import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'mailer_every_monday_at_8_am': {
        'task': 'NewsPortal.tasks.weekly_news_mailer',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        # 'schedule': 60,
    },
}
app.conf.timezone = 'Europe/Moscow'
