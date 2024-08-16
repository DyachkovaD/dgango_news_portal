import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')
app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'daily_email_notification': {
        'task': 'news.tasks.daily_email_notification',
        'schedule': crontab(day_of_week='monday', hour='8'),
    },
}