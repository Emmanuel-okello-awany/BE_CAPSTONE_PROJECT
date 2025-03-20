from django.contrib import admin
from .models import Video

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'uploaded_by', 'uploaded_at')
    search_fields = ('title', 'category')
    list_filter = ('category', 'uploaded_at')

