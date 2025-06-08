
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsConversationParticipant, IsMessageParticipant  

User = get_user_model()

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsConversationParticipant]
    #permission_classes = [IsAuthenticated, IsConversationParticipant]
    filter_backends = [filters.SearchFilter]
    search_fields = ['topic', 'Conversation_type', 'status']

    def get_queryset(self):
        return Conversation.objects.filter(
            participants=self.request.user).prefetch_related('participants', 'message_set')

    def perform_create(self, serializer):
        conversation = serializer.save()
        if self.request.user not in conversation.participants.all():
            conversation.participants.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsMessageParticipant]
    #permission_classes = [IsAuthenticated, IsMessageParticipant]
    filter_backends = [filters.SearchFilter]
    search_fields = ['message_body', 'content']

    def get_queryset(self):
        
        return Message.objects.filter(
            Q(sender=self.request.user) | Q(recipient=self.request.user)
        ).select_related('conversation', 'sender', 'recipient')

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
