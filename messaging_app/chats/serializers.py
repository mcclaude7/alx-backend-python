from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils import timezone
from .models import Conversation, Message

User = get_user_model()
class UserDisplaySerializer(serializers.ModelSerializer):
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

    def validate_birth_date(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("Birth date cannot be in the future.")
        return value

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            'id',  # or 'user_id' if you renamed it
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'phone_number',
            'profile_picture',
            'birth_date'
        ]
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number', ''),
            birth_date=validated_data.get('birth_date', None),
            profile_picture=validated_data.get('profile_picture', None),
        )
        return user

class CustomUserSerializer(serializers.ModelSerializer):
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

    def validate_birth_date(self, value):
        if value > timezone.now().date():
            raise serializers.ValidationError("Birth date cannot be in the future.")
        return value

class MessageSerializer(serializers.ModelSerializer):
    sender = UserDisplaySerializer(read_only=True)
    recipient = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )
    sender_detail = CustomUserSerializer(source='sender', read_only=True)
    recipient_detail = CustomUserSerializer(source='recipient', read_only=True)
    content = serializers.CharField()

    class Meta:
        model = Message
        fields = [
            'message_id',
            'conversation',
            'sender',
            'recipient',
            'sender_detail',
            'recipient_detail',
            'content',
            'sent_at'
        ]


class ConversationSerializer(serializers.ModelSerializer):
    participants = UserDisplaySerializer(many=True, read_only=True)
    #participants = CustomUserSerializer(many=True, read_only=True)
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
            'conversation_type',
            'messages'
        ]

    def get_messages(self, obj):
        # NOTE: To avoid N+1 queries, make sure to prefetch 'message_set' in the view:
        # Conversation.objects.prefetch_related('message_set', 'participants')
        messages = obj.message_set.all().order_by('sent_at')
        return MessageSerializer(messages, many=True).data

    def validate_status(self, value):
        if value not in ['open', 'closed']:
            raise serializers.ValidationError("Status must be either 'open' or 'closed'.")
        return value
