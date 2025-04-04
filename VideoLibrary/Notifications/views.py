from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Notification

@login_required
def notifications_list(request):
    """Render all notifications for the logged-in user."""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'notifications/notifications_list.html', {'notifications': notifications})

@login_required
def notifications_json(request):
    """Return notifications as JSON (for AJAX or frontend fetch)."""
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    data = [{
        'id': n.id,
        'type': n.notification_type,
        'content': n.content,
        'link': n.link,
        'is_read': n.is_read,
        'created_at': n.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for n in notifications]
    return JsonResponse(data, safe=False)
