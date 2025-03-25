from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Count
from .models import Comment
from Video.models import Video
from django.contrib.auth.decorators import login_required

def video_detail(request, video_id):
    video = get_object_or_404(Video, id=video_id)

    # Sorting logic (default to "newest")
    sort_by = request.GET.get("sort", "newest")
    
    if sort_by == "top":
        comments = video.comments.filter(parent=None).annotate(like_count=Count("likes")).order_by("-like_count", "-created_at")
    else:
        comments = video.comments.filter(parent=None).order_by("-created_at")

    return render(request, "video_detail.html", {"video": video, "comments": comments, "sort_by": sort_by})

@login_required
def add_comment(request, video_id):
    if request.method == "POST":
        video = get_object_or_404(Video, id=video_id)
        text = request.POST.get("text")
        parent_id = request.POST.get("parent_id")
        
        if parent_id:
            parent = get_object_or_404(Comment, id=parent_id)
            comment = Comment.objects.create(video=video, user=request.user, text=text, parent=parent)
        else:
            comment = Comment.objects.create(video=video, user=request.user, text=text)

        return redirect("video_detail", video_id=video.id)

@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user

    if user in comment.likes.all():
        comment.likes.remove(user)  # Remove like if already liked
    else:
        comment.likes.add(user)  # Like comment
        comment.dislikes.remove(user)  # Remove dislike if exists

    return JsonResponse({"likes": comment.total_likes(), "dislikes": comment.total_dislikes()})

@login_required
def dislike_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    user = request.user

    if user in comment.dislikes.all():
        comment.dislikes.remove(user)  # Remove dislike if already disliked
    else:
        comment.dislikes.add(user)  # Dislike comment
        comment.likes.remove(user)  # Remove like if exists

    return JsonResponse({"likes": comment.total_likes(), "dislikes": comment.total_dislikes()})
