from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User

@login_required
def delete_user(request):
    user = request.user
    logout(request)  # Log user out first
    user.delete()    # This triggers post_delete signal
    return redirect('home')  # Or wherever you want to redirect

from django.shortcuts import render
from .models import Message
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch


def build_thread(message):
    """Recursive function to fetch replies."""
    return {
        'id': message.id,
        'sender': message.sender.username,
        'receiver': message.receiver.username,
        'content': message.content,
        'timestamp': message.timestamp,
        'replies': [build_thread(reply) for reply in message.replies.all()]
    }

@login_required
def threaded_messages_view(request):
    user = request.user

    # Fetch top-level messages (no parent) for this user
    messages = Message.objects.filter(sender=request.user, receiver__isnull=False, parent_message__isnull=True)\
        .select_related('sender', 'receiver')\
        .prefetch_related(Prefetch('replies', queryset=Message.objects.select_related('sender', 'receiver')))

    # Build threaded view
    threads = [build_thread(message) for message in messages]

    return render(request, 'messaging/threaded_messages.html', {'threads': threads})

@login_required
def unread_inbox_view(request):
    user = request.user
    unread_messages = Message.unread.for_user(user)

    return render(request, 'messaging/unread_inbox.html', {'messages': unread_messages})