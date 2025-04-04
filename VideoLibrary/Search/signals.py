from django.db.models.signals import post_save
from django.dispatch import receiver
from Video.models import Video
from Notifications.models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=Video)
def notify_on_trending_video(sender, instance, **kwargs):
    """Notify uploader if their video is trending."""
    if instance.views >= 10000:  # Example threshold for trending
        notification = Notification.objects.create(
            user=instance.uploader,
            notification_type="trending",
            content=f"Your video '{instance.title}' is now trending!",
            link=f"/video/{instance.id}/"
        )

        # Send WebSocket notification
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"notifications_{instance.uploader.id}",
            {
                "type": "send_notification",
                "message": {
                    "type": "trending",
                    "content": notification.content,
                    "link": notification.link
                },
            }
        )
