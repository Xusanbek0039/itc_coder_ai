from django.core.files.base import ContentFile
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io
from .models import Certificate, CertificateTemplate

class CertificateService:
    @staticmethod
    def generate_certificate(user, course):
        """
        Generates a basic PDF certificate.
        """
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        # Background (if template exists) implementation omitted for brevity
        # Logic: Draw background image if available

        # Text Content
        p.setFont("Helvetica-Bold", 40)
        p.drawCentredString(width / 2, height - 200, "Certificate of Completion")
        
        p.setFont("Helvetica", 20)
        p.drawCentredString(width / 2, height - 300, f"This is to certify that")
        
        p.setFont("Helvetica-Bold", 30)
        p.drawCentredString(width / 2, height - 350, f"{user.first_name} {user.last_name}")
        
        p.setFont("Helvetica", 20)
        p.drawCentredString(width / 2, height - 420, f"Has successfully completed the course:")
        
        p.setFont("Helvetica-Bold", 25)
        p.drawCentredString(width / 2, height - 470, f"{course.title}")
        
        p.setFont("Helvetica", 15)
        p.drawCentredString(width / 2, height - 600, f"Instructor: {course.instructor.get_full_name()}")
        p.drawCentredString(width / 2, height - 630, f"Date: {course.updated_at.strftime('%Y-%m-%d')}") # Should use issued date

        p.showPage()
        p.save()
        
        pdf_name = f"certificate_{user.username}_{course.id}.pdf"
        buffer.seek(0)
        
        # Save to DB
        cert = Certificate(student=user, course=course)
        cert.certificate_file.save(pdf_name, ContentFile(buffer.read()))
        cert.save()
        
        return cert
