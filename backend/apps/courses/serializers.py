from rest_framework import serializers
from .models import Course, Lesson

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'video_url', 'order', 'is_preview', 'created_at']

class CourseSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(source='instructor.username', read_only=True)
    
    # We might not want to show all lessons in list view, but for now it's okay.
    # In a real app we'd have a DetailSerializer.

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'thumbnail', 'instructor_name', 'is_published', 'created_at']

class CourseDetailSerializer(CourseSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta(CourseSerializer.Meta):
        fields = CourseSerializer.Meta.fields + ['lessons']
