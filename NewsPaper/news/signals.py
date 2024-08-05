from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from ..NewsPaper import settings

from .models import PostCategory


def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'new_post_notification.html',
        {
            'text': preview,
            'link': f'http://127.0.0.1:8000/posts/{pk}'
         }
    )
    message = EmailMultiAlternatives(
        subject=title.title(),
        body='',   # пустой, т.к. мы передаём шаблон
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers
    )
    message.attach_alternative(html_content, 'text/html') #text/html - это формат сообщения
    message.send()


@receiver(m2m_changed, sender=PostCategory)
# говорит нам, что письмо будет отправляться только во время соединения
# поста и категории, т.е. добавления нового значения в таблицу PostCategory
def notify_new_post(sender, instance, **kwargs): # instance - это сама новая статья
    if kwargs['action'] == 'post_add':           # нас интересуют случаи создания новой статьи, не изменения
        categories = instance.category.all()
        subscribers_emails = []

        for cat in categories:
            subscribers = cat.subscribers.all()
            subscribers_emails += [s.email for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.title, subscribers_emails)