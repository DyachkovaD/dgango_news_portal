from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.shortcuts import redirect

from datetime import date, datetime

from .models import PostCategory, Post


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
# говорит нам, что письмо будет отправляться только во время соединения
# поста и категории, т.е. добавления нового значения в таблицу PostCategory
def notify_new_post(sender, instance, **kwargs): # instance - это сама новая статья
    if kwargs['action'] == 'post_add':           # нас интересуют случаи создания новой статьи, не изменения
        categories = instance.category.all()
        # subscribers_emails = []
        subscribers = set()

        for cat in categories:
            cat_subscribers = cat.subscribers.all()
            if cat_subscribers:
                subscribers.add(*cat_subscribers)
            # subscribers_emails += [s.email for s in subscribers]

        send_notifications(instance.text, instance.pk, instance.title, subscribers)


# @receiver(pre_save, sender=Post, )
# def post3_limit(sender, instance, **kwargs):
#     posts_today = len(Post.objects.filter(author=instance.author, date__day=datetime.today().day))
#     if posts_today >= 3:
#         raise ValidationError("Вы не можете создавать более трёх постов в день.")
#     else:
#         return instance
