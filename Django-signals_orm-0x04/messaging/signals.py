from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from .models import Message, MessageHistory, Notification
from django.contrib.auth.models import User

# Signal to create a Notification when a new message is created
@receiver(post_save, sender=Message)
def create_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )

# Signal to track message edits
@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.id:
        try:
            old_message = Message.objects.get(id=instance.id)
            if old_message.content != instance.content:
                # Attempt to preserve previous content
                MessageHistory.objects.create(
                    message=old_message,
                    old_content=old_message.content,
                    # edited_by = ??? — requires explicit context like request.user
                )
                instance.edited = True
        except Message.DoesNotExist:
            pass

@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    # Delete sent and received messages
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()
    
    # Delete notifications
    Notification.objects.filter(user=instance).delete()
    
    # Delete all message histories edited by the user
    MessageHistory.objects.filter(edited_by=instance).delete()
