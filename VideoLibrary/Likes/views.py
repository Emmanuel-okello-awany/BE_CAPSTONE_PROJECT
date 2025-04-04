from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Reaction
from Video.models import Video
from Comments.models import Comment 


@login_required
def react_to_video(request, video_id, reaction_type):
    video = get_object_or_404(Video, id=video_id)
    
    # Remove any existing reaction from this user for the same video
    existing_reaction = Reaction.objects.filter(user=request.user, video=video)

    if existing_reaction.exists():
        if existing_reaction.first().reaction_type == reaction_type:
            existing_reaction.delete()  # Remove reaction if same type (toggle off)
            return JsonResponse({'reaction': 'removed', 'likes_count': video.reaction_set.filter(reaction_type="like").count(), 'dislikes_count': video.reaction_set.filter(reaction_type="dislike").count()})
        else:
            existing_reaction.update(reaction_type=reaction_type)  # Switch reaction
    else:
        Reaction.objects.create(user=request.user, video=video, reaction_type=reaction_type)  # New reaction

    return JsonResponse({'reaction': reaction_type, 'likes_count': video.reaction_set.filter(reaction_type="like").count(), 'dislikes_count': video.reaction_set.filter(reaction_type="dislike").count()})



@login_required
def react_to_comment(request, comment_id, reaction_type):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Remove any existing reaction from this user for the same comment
    existing_reaction = Reaction.objects.filter(user=request.user, comment=comment)

    if existing_reaction.exists():
        if existing_reaction.first().reaction_type == reaction_type:
            existing_reaction.delete()  # Remove reaction if same type (toggle off)
            return JsonResponse({
                'reaction': 'removed',
                'likes_count': comment.reaction_set.filter(reaction_type="like").count(),
                'dislikes_count': comment.reaction_set.filter(reaction_type="dislike").count()
            })
        else:
            existing_reaction.update(reaction_type=reaction_type)  # Switch reaction
    else:
        Reaction.objects.create(user=request.user, comment=comment, reaction_type=reaction_type)  # New reaction

    return JsonResponse({
        'reaction': reaction_type,
        'likes_count': comment.reaction_set.filter(reaction_type="like").count(),
        'dislikes_count': comment.reaction_set.filter(reaction_type="dislike").count()
    })
