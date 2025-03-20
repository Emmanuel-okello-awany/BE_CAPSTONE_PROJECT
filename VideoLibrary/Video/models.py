from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    category = models.CharField(max_length=100, choices=[
        ('Music', 'Music'),
        ('Sports', 'Sports'),
        ('Education', 'Education'),
        ('Movies', 'Movies'),
    ], default='Education')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

