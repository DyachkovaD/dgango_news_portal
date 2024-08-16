from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from .models import PostCategory
from .tasks import new_post_notification


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
            body='',   # пустой, т.к. мы передаём шаблон
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        message.attach_alternative(html_content, 'text/html') #text/html - это формат сообщения
        message.send()


@receiver(m2m_changed, sender=PostCategory, )
def notify_new_post(sender, instance, **kwargs): # instance - это сама новая статья
    if kwargs['action'] == 'post_add':           # нас интересуют случаи создания новой статьи, не изменения
        new_post_notification(instance.pk)

        categories = instance.category.all()
        subscribers = set()

        for cat in categories:
            cat_subscribers = cat.subscribers.all()
            if cat_subscribers:
                subscribers.update(set(cat_subscribers))

        send_notifications(instance.text, instance.pk, instance.title, subscribers)
