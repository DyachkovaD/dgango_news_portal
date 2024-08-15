import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')
app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.timezone = 'UTC'
app.conf.beat_schedule = {
    'hello_every_3_sec': {
        'task': 'tasks.hello',
        'schedule': crontab(minute='*/1'),
    },
}

# app.conf.beat_schedule = {
#     'daily_email_notification': {
#         'task': 'tasks.daily_email_notification',
#         'schedule': crontab(minute='10', hour='15', day_of_week='thu'),
#     },
# }
#
# app.conf.beat_schedule = {
#     'new_post_email_notification': {
#         'task': 'tasks.new_post_notification',
#         'schedule': 1,
#     },
# }