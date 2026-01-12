from rest_framework import serializers
from .models import Enrollment, LessonProgress
from courses.serializers import CourseSerializer, LessonSerializer

class LessonProgressSerializer(serializers.ModelSerializer):
    lesson_id = serializers.IntegerField(source='lesson.id', read_only=True)
    title = serializers.CharField(source='lesson.title', read_only=True)
    order = serializers.IntegerField(source='lesson.order', read_only=True)

    class Meta:
        model = LessonProgress
        fields = ['id', 'lesson_id', 'title', 'order', 'status', 'completed_at']

class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    progress = LessonProgressSerializer(source='lesson_progress', many=True, read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'course', 'enrolled_at', 'is_completed', 'progress']
