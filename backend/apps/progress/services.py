from django.db import transaction
from .models import LessonProgress, Enrollment
from courses.models import Lesson

class ProgressService:
    @staticmethod
    def initialize_enrollment(user, course):
        """
        Creates enrollment and unlocks the first lesson.
        """
        enrollment, created = Enrollment.objects.get_or_create(student=user, course=course)
        
        if created:
            # Create Progress entries for all lessons
            lessons = course.lessons.all().order_by('order')
            progress_list = []
            for index, lesson in enumerate(lessons):
                status = LessonProgress.Status.UNLOCKED if index == 0 else LessonProgress.Status.LOCKED
                progress_list.append(LessonProgress(
                    enrollment=enrollment,
                    lesson=lesson,
                    status=status
                ))
            LessonProgress.objects.bulk_create(progress_list)
        
        return enrollment

    @staticmethod
    def complete_lesson(enrollment, lesson):
        """
        Marks lesson as complete and unlocks the next one.
        """
        # 1. Mark current lesson as COMPLETED
        current_progress = LessonProgress.objects.get(enrollment=enrollment, lesson=lesson)
        current_progress.status = LessonProgress.Status.COMPLETED
        current_progress.save()

        # 2. Check for next lesson
        next_lesson = Lesson.objects.filter(
            course=enrollment.course, 
            order__gt=lesson.order
        ).order_by('order').first()

        if next_lesson:
            next_progress, _ = LessonProgress.objects.get_or_create(enrollment=enrollment, lesson=next_lesson)
            if next_progress.status == LessonProgress.Status.LOCKED:
                next_progress.status = LessonProgress.Status.UNLOCKED
                next_progress.save()
        else:
            # No more lessons -> Course Completed?
            # Check if all lessons are completed
            total_lessons = enrollment.course.lessons.count()
            completed_count = LessonProgress.objects.filter(
                enrollment=enrollment, 
                status=LessonProgress.Status.COMPLETED
            ).count()
            
            if total_lessons == completed_count:
                enrollment.is_completed = True
                enrollment.save()
                # TODO: Trigger Certificate Generation here
                
        return current_progress
