from rest_framework import views, status, permissions
from rest_framework.response import Response
from .services import AIService

class AIChatView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        POST /api/v1/ai/chat/
        Body: { "lesson_id": 1, "message": "Help me understand hooks" }
        """
        lesson_id = request.data.get('lesson_id')
        message = request.data.get('message')

        if not lesson_id or not message:
            return Response(
                {'error': 'lesson_id and message are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # In a real app, check if user has access to this lesson via ProgressService/IsEnrolled
        
        response_text = AIService.get_tutor_response(request.user, lesson_id, message)
        return Response({'reply': response_text})
