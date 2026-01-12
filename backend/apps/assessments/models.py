from django.db import models
from django.conf import settings
from courses.models import Lesson

User = settings.AUTH_USER_MODEL

class Assignment(models.Model):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, related_name='assignment')
    title = models.CharField(max_length=255)
    instructions = models.TextField()
    
    def __str__(self):
        return self.title

class AssignmentSubmission(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'

    assignment = models.ForeignKey(Assignment, related_name='submissions', on_delete=models.CASCADE)
    student = models.ForeignKey(User, related_name='assignments', on_delete=models.CASCADE)
    content = models.TextField(blank=True, help_text="Text submission")
    file = models.FileField(upload_to='assignments/submissions/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    feedback = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.assignment.title}"

class Quiz(models.Model):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, related_name='quiz')
    title = models.CharField(max_length=255)
    passing_score = models.PositiveIntegerField(default=70, help_text="Percentage required to pass")

    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    options = models.JSONField(help_text="List of options, e.g. ['A', 'B', 'C', 'D']")
    correct_answer = models.CharField(max_length=255, help_text="Must match one of the options")

    def __str__(self):
        return self.text[:50]

class QuizAttempt(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='attempts', on_delete=models.CASCADE)
    student = models.ForeignKey(User, related_name='quiz_attempts', on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    passed = models.BooleanField(default=False)
    attempted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.quiz.title} ({self.score}%)"
