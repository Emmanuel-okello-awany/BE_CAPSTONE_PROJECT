from django.db.models.signals import post_save
from django.dispatch import receiver
from Comments.models import Comment
from Notifications.models import Notification
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

@receiver(post_save, sender=Comment)
def notify_on_comment(sender, instance, created, **kwargs):
    """Notify the video uploader when a new comment is added."""
    if created:
        notification_user = instance.video.uploader  # Video owner
        if instance.parent:  # If it's a reply
            notification_user = instance.parent.user  # Notify original commenter

        notification = Notification.objects.create(
            user=notification_user,
            notification_type="comment",
            content=f"{instance.user.username} commented on your video '{instance.video.title}'",
            link=f"/video/{instance.video.id}/#comment-{instance.id}"
        )

        # Send WebSocket notification
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"notifications_{notification_user.id}",
            {
                "type": "send_notification",
                "message": {
                    "type": "comment",
                    "content": notification.content,
                    "link": notification.link
                },
            }
        )
