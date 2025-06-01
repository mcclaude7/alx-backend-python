from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Conversation, Message

User = get_user_model()

class CustomUserSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    class Meta:
        model = User
        fields = [
            'user_id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
            'profile_picture',
            'birth_date'
        ]

class MessageSerializer(serializers.ModelSerializer):
    sender = CustomUserSerializer(read_only=True)
    recipient = CustomUserSerializer(read_only=True)

    message_body = serializers.CharField()
    content = serializers.CharField()

    class Meta:
        model = Message
        fields = [
            'message_id',
            'conversation',
            'message_body',
            'sender',
            'recipient',
            'content',
            'sent_at'
        ]

class ConversationSerializer(serializers.ModelSerializer):
    participants = CustomUserSerializer(many=True, read_only=True)
    topic = serializers.CharField(allow_blank=True, required=False)
    messages = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'created_at',
            'updated_at',
            'status',
            'topic',
            'Conversation_type',
            'messages'
        ]

    def get_messages(self, obj):
        messages = obj.message_set.all().order_by('sent_at')
        return MessageSerializer(messages, many=True).data

    def validate_status(self, value):
        if value not in ['open', 'closed']:
            raise serializers.ValidationError("Status must be either 'open' or 'closed'.")
        return value

