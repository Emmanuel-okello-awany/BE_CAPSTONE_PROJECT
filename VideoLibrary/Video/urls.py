from django.urls import path
from .views import (
    video_list, video_detail, upload_video, delete_video,
    VideoListCreateAPI, VideoDetailAPI, api_upload_video, api_increment_views, browse_videos, watch_video
)

urlpatterns = [
    # Web views
    path('', video_list, name='video_list'),
    path('details/<int:video_id>/', video_detail, name='video_detail'),
    path('upload/', upload_video, name='upload_video'),
    path('delete/<int:video_id>/', delete_video, name='delete_video'),
    path('browse/', browse_videos, name='browse_videos'),
    path("videos/<int:video_id>/", watch_video, name="watch_video"),
    path('<slug:slug>/', video_detail, name='video_detail'),


    # API views
    path('api/videos/', VideoListCreateAPI.as_view(), name='video-list-api'),
    path('api/videos/<int:pk>/', VideoDetailAPI.as_view(), name='video-detail-api'),
    path('api/upload/', api_upload_video, name='upload-video-api'),
    path('api/videos/<int:video_id>/increment_views/', api_increment_views, name='increment-views-api'),
]
