from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model 

User = get_user_model
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.username
User = get_user_model()   
class Conversation(models.Model):
    participants= models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=[('open', 'Open'),('closed', 'Closed')])
    topic = models.CharField(max_length=100, blank=True, null=True)
    Conversation_type = models.CharField(max_length=20, choices=[('private','Private'),('group','Group'),('support','Support')], default='private', null=True, blank=True)

    def __str__(self):
        return self.Conversation_type

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient} at {self.timestamp}"

# Create your models here.
