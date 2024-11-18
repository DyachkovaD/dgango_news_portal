from django.core.exceptions import PermissionDenied
from django.db.models.signals import m2m_changed, pre_save
from django.dispatch import receiver
from datetime import datetime
from django.shortcuts import redirect

from .models import PostCategory, Post
from .tasks import new_post_notification


@receiver(m2m_changed, sender=PostCategory, )
def notify_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':           # нас интересуют случаи создания новой статьи, не изменения
        new_post_notification.delay(instance.pk)


# @receiver(pre_save, sender=Post, )
# def post_3_day_limit(sender, instance, **kwargs):
#     if not instance.pk:
#         author = instance.author
#         posts_today = len(Post.objects.filter(author=author, date__day=datetime.today().day))
#         if posts_today >= 3:
#             return PermissionDenied
