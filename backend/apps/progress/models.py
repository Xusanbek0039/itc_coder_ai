from django.db import models
from django.conf import settings
from courses.models import Course, Lesson

User = settings.AUTH_USER_MODEL

class Enrollment(models.Model):
    student = models.ForeignKey(User, related_name='enrollments', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='enrollments', on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ['student', 'course']

    def __str__(self):
        return f"{self.student.username} -> {self.course.title}"

class LessonProgress(models.Model):
    class Status(models.TextChoices):
        LOCKED = 'LOCKED', 'Locked'
        UNLOCKED = 'UNLOCKED', 'Unlocked'
        COMPLETED = 'COMPLETED', 'Completed'

    enrollment = models.ForeignKey(Enrollment, related_name='lesson_progress', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.LOCKED)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['enrollment', 'lesson']

    def __str__(self):
        return f"{self.enrollment.student.username} - {self.lesson.title}: {self.status}"
