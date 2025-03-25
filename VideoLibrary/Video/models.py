from django.db import models
from django.utils.text import slugify
from django.contrib.auth import get_user_model

User = get_user_model()

class Video(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True, null=True)  
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='videos/')
    thumbnail = models.ImageField(
        upload_to='thumbnails/',
        blank=True,
        null=True,
        default='thumbnails/default-thumbnail.jpg'  
    )
    category = models.CharField(max_length=100, choices=[
        ('Music', 'Music'),
        ('Sports', 'Sports'),
        ('Education', 'Education'),
        ('Movies', 'Movies'),
        ('Gaming', 'Gaming'),
        ('Technology', 'Technology'),
    ], default='Education')
    tags = models.CharField(max_length=255, blank=True, help_text="Comma-separated tags")  # For better search filtering
    views = models.PositiveIntegerField(default=0)  # Track video views
    is_public = models.BooleanField(default=True)  # Visibility toggle (public/private)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="videos")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Generate slug automatically
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """ Returns the URL of the video detail page """
        return f"/videos/{self.slug}/"
