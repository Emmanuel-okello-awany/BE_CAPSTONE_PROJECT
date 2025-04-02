from django.urls import path
from .views import search_videos, browse_videos

urlpatterns = [
    path('api/', search_videos, name='search_api'),  # API search
    path('', browse_videos, name='browse'),  # Web search page
]
