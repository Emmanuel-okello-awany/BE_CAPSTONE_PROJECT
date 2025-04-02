from rest_framework import serializers
from Video.models import Video  

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = ['id', 'title', 'description', 'thumbnail', 'uploaded_at', 'video_file']
