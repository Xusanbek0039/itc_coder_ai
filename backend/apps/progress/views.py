from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Enrollment, LessonProgress
from courses.models import Course, Lesson
from .serializers import EnrollmentSerializer, LessonProgressSerializer
from .services import ProgressService

class EnrollmentViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EnrollmentSerializer

    def get_queryset(self):
        return Enrollment.objects.filter(student=self.request.user)

    @action(detail=False, methods=['post'])
    def enroll(self, request):
        """
        POST /api/v1/progress/enroll/
        Body: { "course_id": 1 }
        """
        course_id = request.data.get('course_id')
        if not course_id:
            return Response({'error': 'course_id required'}, status=status.HTTP_400_BAD_REQUEST)
        
        course = get_object_or_404(Course, pk=course_id)
        enrollment = ProgressService.initialize_enrollment(request.user, course)
        return Response(EnrollmentSerializer(enrollment).data, status=status.HTTP_201_CREATED)

class LessonCompletionView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LessonProgressSerializer

    def patch(self, request, lesson_id):
        """
        PATCH /api/v1/progress/lessons/<id>/complete/
        """
        lesson = get_object_or_404(Lesson, pk=lesson_id)
        enrollment = get_object_or_404(Enrollment, student=request.user, course=lesson.course)
        
        # Check logic via Service
        progress = ProgressService.complete_lesson(enrollment, lesson)
        
        return Response(LessonProgressSerializer(progress).data)
