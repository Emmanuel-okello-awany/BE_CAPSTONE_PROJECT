from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Reaction
from Notifications.models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=Reaction)
def notify_on_like(sender, instance, created, **kwargs):
    """Notify user when their video gets liked."""
    if created:
        notification = Notification.objects.create(
            user=instance.video.uploader,
            notification_type="like",
            content=f"Your video '{instance.video.title}' received a like!",
            link=f"/video/{instance.video.id}/"
        )

        # Send WebSocket notification
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"notifications_{instance.video.uploader.id}",
            {
                "type": "send_notification",
                "message": {
                    "type": "like",
                    "content": notification.content,
                    "link": notification.link
                },
            }
        )

@receiver(post_delete, sender=Reaction)
def notify_on_like_removed(sender, instance, **kwargs):
    """Optional: Notify when a like is removed (if needed)."""
