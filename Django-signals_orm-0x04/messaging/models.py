
# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Prefetch

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    parent_message = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    def get_user_conversations(user):
        messages = Message.objects.filter(receiver=user, parent_message__isnull=True)\
            .select_related('sender', 'receiver')\
            .prefetch_related(Prefetch('replies', queryset=Message.objects.select_related('sender')))
        return messages
    def fetch_thread(message):
      
      thread = {
        'id': message.id,
        'content': message.content,
        'sender': message.sender.username,
        'timestamp': message.timestamp,
        'replies': []
        }
      for reply in message.replies.all().select_related('sender'):
        thread['replies'].append(fetch_thread(reply))
      return thread


    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}: {self.content[:20]}"

class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='edited_histories')

    def __str__(self):
        return f"Edit history of Message ID {self.message.id}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} - Message ID: {self.message.id}"
