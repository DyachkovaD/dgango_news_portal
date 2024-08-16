from celery import shared_task
import datetime

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from .models import Post, Category


def send_notifications(text, pk, title, subscribers):
    for user in subscribers:
        html_content = render_to_string(
            'new_post_notification.html',
            {
                'username': user.username,
                'text': text,
                'link': f'http://127.0.0.1:8000/posts/{pk}'
                }
        )
        message = EmailMultiAlternatives(
            subject=title,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        message.attach_alternative(html_content, 'text/html')
        message.send()


@shared_task
def new_post_notification(pk):
            post = Post.objects.get(pk=pk)
            categories = post.category.all()
            subscribers = set()

            for cat in categories:
                cat_subscribers = cat.subscribers.all()
                if cat_subscribers:
                    subscribers.add(*cat_subscribers)
            send_notifications(post.text, post.pk, post.title, subscribers)


@shared_task
def daily_email_notification():
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)
    posts = Post.objects.filter(date__gte=last_week)
    categories = posts.values_list('category__name', flat=True)

    for category in categories:
        subscribers = set(Category.objects.filter(name=category).values_list('subscribers__email', flat=True))
        cat_posts = posts.filter(category__name=category)

        html_content = render_to_string(
            'daily_post.html',
            {
                'link': 'http://127.0.0.1:8000/',
                'posts': cat_posts,
            }
        )

        msg = EmailMultiAlternatives(
            subject='Статьи за неделю',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=subscribers
        )

        msg.attach_alternative(html_content, 'text/html')
        msg.send()