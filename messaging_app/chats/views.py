
from rest_framework import viewsets, status, filters, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer, UserCreateSerializer, UserDisplaySerializer
from .permissions import IsConversationParticipant, IsMessageParticipant  
from django_filters.rest_framework import DjangoFilterBackend
from .filters import MessageFilter
from .pagination import MessagePagination
from chats import serializers

User = get_user_model()

class UserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    def get_serializer_class(self):
        if self.action in ['create']:
            return UserCreateSerializer
        return UserDisplaySerializer

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsConversationParticipant]
    filter_backends = [filters.SearchFilter]
    search_fields = ['topic', 'Conversation_type', 'status']

    def get_queryset(self):
        return Conversation.objects.filter(
            participants=self.request.user
            ).prefetch_related('participants', 'message_set')

    def perform_create(self, serializer):
        conversation = serializer.save()
        if self.request.user not in conversation.participants.all():
            conversation.participants.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsMessageParticipant] 
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class = MessageFilter
    pagination_class = MessagePagination
    search_fields = ['content']

    def get_queryset(self):    
        return Message.objects.filter(
            Q(sender=self.request.user) | Q(recipient=self.request.user)
        ).select_related('conversation', 'sender', 'recipient')
    
    def perform_create(self, serializer):
        conversation_id = self.request.data.get('conversation')
        recipient_id = self.request.data.get('recipient')
        conversation = get_object_or_404(Conversation, id=conversation_id)
        #conversation = get_object_or_404(Conversation, conversation_id=conversation_id)
        recipient = get_object_or_404(User, pk=recipient_id)

        if self.request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant of this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )
        if recipient not in conversation.participants.all():
            raise serializers.ValidationError('Recipient is not a participant of the conversation.')

        serializer.save(sender=self.request.user)
    
