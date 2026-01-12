import openai
from django.conf import settings
from courses.models import Lesson

class AIService:
    @staticmethod
    def get_tutor_response(user, lesson_id, message):
        """
        Calls OpenAI API to act as a tethered tutor.
        """
        try:
            lesson = Lesson.objects.get(id=lesson_id)
            course_title = lesson.course.title
            
            # System Prompt Engineering
            system_prompt = (
                f"You are an expert AI Tutor for the course '{course_title}'. "
                f"The student is currently on the lesson: '{lesson.title}'. "
                f"Context from lesson description: {lesson.description}. "
                "Your goal is to help the student understand the material. "
                "RULES: "
                "1. Be encouraging and helpful. "
                "2. Do NOT give direct answers to quizzes or assignments. Instead, guide them. "
                "3. Explain concepts simply and step-by-step. "
                "4. Keep responses concise (under 200 words) where possible."
            )

            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            
            response = client.chat.completions.create(
                model="gpt-4o", # or gpt-3.5-turbo
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                temperature=0.7,
                max_tokens=300
            )

            return response.choices[0].message.content

        except Lesson.DoesNotExist:
            return "Error: Lesson context not found."
        except Exception as e:
            return f"Error connecting to AI Tutor: {str(e)}"
