from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()  

    class Meta:
        model = Comment
        fields = ['id', 'video', 'user', 'text', 'created_at']
        read_only_fields = ['user', 'created_at']
