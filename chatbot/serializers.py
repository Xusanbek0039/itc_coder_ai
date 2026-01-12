from rest_framework import serializers
from .models import ChatSession, ChatMessage

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'message', 'image', 'created_at']

class ChatSessionSerializer(serializers.ModelSerializer):
    messages = ChatMessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = ChatSession
        fields = ['id', 'user', 'created_at', 'updated_at', 'messages']
        read_only_fields = ['user']

class ChatInputSerializer(serializers.Serializer):
    message = serializers.CharField(required=False, allow_blank=True)
    image = serializers.ImageField(required=False)
    session_id = serializers.IntegerField(required=False)
