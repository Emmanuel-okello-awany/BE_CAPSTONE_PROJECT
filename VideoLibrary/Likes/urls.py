from django.urls import path
from .views import react_to_video, react_to_comment

urlpatterns = [
    path('video-react/<int:video_id>/<str:reaction_type>/', react_to_video, name='react_to_video'),
    path('comment-react/<int:comment_id>/<str:reaction_type>/', react_to_comment, name='react_to_comment'),

]
