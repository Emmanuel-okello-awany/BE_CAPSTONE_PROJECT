from django.urls import path
from .views import video_detail, add_comment, like_comment, dislike_comment

urlpatterns = [
    path('video/<int:video_id>/', video_detail, name='video_detail'),
    path('video/<int:video_id>/comment/', add_comment, name='add_comment'),
    path('comment/<int:comment_id>/like/', like_comment, name='like_comment'),
    path('comment/<int:comment_id>/dislike/', dislike_comment, name='dislike_comment'),
]
