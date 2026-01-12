from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Certificate
from rest_framework import serializers

class CertificateSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='course.title', read_only=True)
    class Meta:
        model = Certificate
        fields = ['id', 'course_title', 'issued_at', 'certificate_file', 'unique_id']

class CertificateListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CertificateSerializer

    def get_queryset(self):
        return Certificate.objects.filter(student=self.request.user)

# Generation trigger usually happens in ProgressService, not an endpoint
