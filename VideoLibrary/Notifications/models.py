from django.db import models
from django.contrib.auth import get_user_model
from Video.models import Video
from Comments.models import Comment

User = get_user_model()

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('like', 'Liked your video'),
        ('dislike', 'Disliked your video'),
        ('comment', 'Commented on your video'),
        ('reply', 'Replied to your comment'),
        ('view', 'Viewed your video'),
    ]

    sender = models.ForeignKey(User, related_name='sent_notifications', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sender} {self.get_notification_type_display()} to {self.recipient}"
