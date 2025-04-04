from django.db import models
from django.contrib.auth import get_user_model
from Video.models import Video
from Comments.models import Comment  

User = get_user_model()

class Reaction(models.Model):
    REACTION_CHOICES = [
        ('like', 'Like'),
        ('dislike', 'Dislike'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'video')  
    def __str__(self):
        return f"{self.user} {self.reaction_type}d {self.video}"
