from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import PostCategory
from .tasks import new_post_notification


@receiver(m2m_changed, sender=PostCategory, )
def notify_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':           # нас интересуют случаи создания новой статьи, не изменения
        new_post_notification.delay(instance.pk)

