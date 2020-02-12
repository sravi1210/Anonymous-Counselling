from django.contrib import admin
from django.urls import path, include
from . import views
from .models import counsellor
from django.views.generic.base import TemplateView
from uuid import uuid4

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('update/', views.Update.as_view(), name='update'),
    path('chatroom/<uuid:chatroom_id>', views.Chat, name='chatroom'),
    path('studentCounselling/', views.studentCounselling, name='studentCounselling'),
    path('Recent/', views.Recent, name='Recent'),
    path('chatroom_refresh/<uuid:chatroom_id>', views.messagerefresh, name='chatroomrefresh'),
    path('counsellor',TemplateView.as_view(template_name='counsellor.html'), name='counsellor'),
    path('student',TemplateView.as_view(template_name='student.html'), name='student'),
    path('waiting_students', views.available_chatroom, name='waiting_students'),
]
