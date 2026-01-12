import google.generativeai as genai
import os
from django.conf import settings
from PIL import Image

def get_ai_response(text, image_path=None):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Error: Gemini API Key not configured."
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    parts = []
    if text:
        parts.append(text)
    
    if image_path:
        # image_path is absolute path from Django request or media root
        try:
            img = Image.open(image_path)
            parts.append(img)
        except Exception as e:
            return f"Error opening image: {str(e)}"

    if not parts:
        return "Please provide text or an image."

    try:
        response = model.generate_content(parts)
        return response.text
    except Exception as e:
        return f"AI Error: {str(e)}"
