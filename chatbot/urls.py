from django.urls import path
from .views import ChatView

urlpatterns = [
    path('chat/', ChatView.as_view(), name='chat_list_create'),
    path('chat/<int:session_id>/', ChatView.as_view(), name='chat_detail'),
]
