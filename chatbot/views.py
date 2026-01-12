from rest_framework import views, status, permissions
from rest_framework.response import Response
from .models import ChatSession, ChatMessage
from .serializers import ChatSessionSerializer, ChatMessageSerializer, ChatInputSerializer
from .services import get_ai_response
from django.shortcuts import get_object_or_404

class ChatView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, session_id=None):
        if session_id:
            session = get_object_or_404(ChatSession, id=session_id, user=request.user)
            serializer = ChatSessionSerializer(session)
            return Response(serializer.data)
        
        sessions = ChatSession.objects.filter(user=request.user).order_by('-created_at')
        serializer = ChatSessionSerializer(sessions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ChatInputSerializer(data=request.data)
        if serializer.is_valid():
            session_id = serializer.validated_data.get('session_id')
            text = serializer.validated_data.get('message', '')
            image = serializer.validated_data.get('image')

            # Get or Create Session
            if session_id:
                session = get_object_or_404(ChatSession, id=session_id, user=request.user)
            else:
                session = ChatSession.objects.create(user=request.user)

            # Save User Message
            user_msg = ChatMessage.objects.create(
                session=session,
                sender='user',
                message=text,
                image=image
            )

            # Process with AI
            image_path = user_msg.image.path if user_msg.image else None
            ai_reply_text = get_ai_response(text, image_path)

            # Save Bot Message
            bot_msg = ChatMessage.objects.create(
                session=session,
                sender='bot',
                message=ai_reply_text
            )

            return Response({
                'session_id': session.id,
                'user_message': ChatMessageSerializer(user_msg).data,
                'bot_response': ChatMessageSerializer(bot_msg).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
