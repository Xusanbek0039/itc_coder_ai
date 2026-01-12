import uuid
from django.db import models
from django.conf import settings
from courses.models import Course

User = settings.AUTH_USER_MODEL

class CertificateTemplate(models.Model):
    name = models.CharField(max_length=100)
    background_image = models.ImageField(upload_to='certificates/templates/')
    font_color = models.CharField(max_length=7, default="#000000", help_text="Hex code")
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Certificate(models.Model):
    student = models.ForeignKey(User, related_name='certificates', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='certificates', on_delete=models.CASCADE)
    issued_at = models.DateTimeField(auto_now_add=True)
    certificate_file = models.FileField(upload_to='certificates/issued/')
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    class Meta:
        unique_together = ['student', 'course']

    def __str__(self):
        return f"Certificate: {self.student.username} - {self.course.title}"
