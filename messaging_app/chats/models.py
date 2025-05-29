import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model 

#User = get_user_model
class CustomUser(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Stored hashed
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username
    
User = get_user_model()   
class Conversation(models.Model):
    conversation_id = models.AutoField(primary_key=True)
    participants= models.ManyToManyField(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=[('open', 'Open'),('closed', 'Closed')])
    topic = models.CharField(max_length=100, blank=True, null=True)
    Conversation_type = models.CharField(max_length=20, choices=[('private','Private'),('group','Group'),('support','Support')], default='private', null=True, blank=True)

    def __str__(self):
        return self.conversation_id

class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, null=True, blank=True)
    Message_body = models.TextField(null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient} at {self.timestamp}"

# Create your models here.
