from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=Notification)
def send_notification_via_websocket(sender, instance, created, **kwargs):
    """Send new notifications to the user via WebSockets."""
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"notifications_{instance.user.id}",
            {
                "type": "send_notification",
                "message": {
                    "type": instance.notification_type,
                    "content": instance.content,
                    "link": instance.link
                },
            }
        )
