from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Video
from .serializers import VideoSerializer
from .forms import VideoUploadForm

# ------------------------- WEB VIEWS (HTML) -------------------------

def video_list(request):
    """Display all videos in a paginated view."""
    videos = Video.objects.all().order_by('-uploaded_at')
    paginator = Paginator(videos, 9)  # 9 videos per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'video/video_list.html', {'page_obj': page_obj})

def video_detail(request, video_id):
    """Display a single video with details."""
    video = get_object_or_404(Video, id=video_id)
    video.views += 1  # Increment views count
    video.save()
    return render(request, 'video/video_detail.html', {'video': video})

def watch_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    return render(request, "video/watch_video.html", {"video": video})


def browse_videos(request):
    """Display all uploaded videos in a grid format with pagination and category filtering."""
    
    # Extract predefined categories from the model choices
    categories = [choice[0] for choice in Video._meta.get_field('category').choices]

    # Get selected category from request
    category_filter = request.GET.get('category')
    
    # Fetch videos and apply category filter if selected
    videos = Video.objects.all().order_by('-uploaded_at')
    if category_filter and category_filter in categories:
        videos = videos.filter(category=category_filter)

    # Implement pagination (9 videos per page)
    paginator = Paginator(videos, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'video/browse.html', {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_filter  # Pass selected category for highlighting
    })



@login_required  
def upload_video(request):
    if request.method == "POST":
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)  
            video.uploaded_by = request.user  # Assign current logged-in user
            video.save()  
            return redirect("video_list")  # Redirect to video list 
    else:
        form = VideoUploadForm()
    return render(request, "video/upload_video.html", {"form": form})

@login_required
def delete_video(request, video_id):
    """Delete a video."""
    video = get_object_or_404(Video, id=video_id)
    if request.user.is_superuser or request.user == video.uploader:
        video.delete()
        messages.success(request, "Video deleted successfully!")
        return redirect('video_list')
    else:
        messages.error(request, "You do not have permission to delete this video.")
        return redirect('video_detail', video_id=video.id)

# ------------------------- API VIEWS (JSON) -------------------------

class VideoListCreateAPI(generics.ListCreateAPIView):
    """API endpoint for listing and creating videos."""
    queryset = Video.objects.all().order_by('-uploaded_at')
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class VideoDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    """API endpoint for retrieving, updating, and deleting a video."""
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def api_upload_video(request):
    """API endpoint for uploading videos."""
    serializer = VideoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@csrf_exempt
def api_increment_views(request, video_id):
    """API endpoint to increase the view count of a video."""
    video = get_object_or_404(Video, id=video_id)
    video.views += 1
    video.save()
    return JsonResponse({'message': 'View count updated', 'views': video.views})
