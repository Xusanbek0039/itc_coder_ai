from rest_framework import viewsets, permissions
from .models import Course, Lesson
from .serializers import CourseSerializer, CourseDetailSerializer, LessonSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.filter(is_published=True)
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CourseDetailSerializer
        return CourseSerializer

    def perform_create(self, serializer):
        # Check if user is teacher? handled by permission usually
        serializer.save(instructor=self.request.user)

# LessonViewSet might be nested or separate. 
# For now, CourseDetail includes lessons. 
# If we want a separate endpoint for lessons (e.g. /courses/1/lessons/), we can add it.
