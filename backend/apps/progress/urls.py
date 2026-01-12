from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EnrollmentViewSet, LessonCompletionView

router = DefaultRouter()
router.register('', EnrollmentViewSet, basename='enrollments')

urlpatterns = [
    path('lessons/<int:lesson_id>/complete/', LessonCompletionView.as_view(), name='lesson-complete'),
    path('', include(router.urls)),
]
