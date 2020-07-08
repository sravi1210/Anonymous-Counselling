from django.contrib import admin
from django.urls import path, include
from . import views
from .models import counsellor
from django.views.generic.base import TemplateView
from uuid import uuid4

urlpatterns = [
    path('update/', views.Update.as_view(), name='update'),
    # this is for cousellor to update his info ,
    path('chatroom/<uuid:chatroom_id>', views.Chat, name='chatroom'),
    # this is the chatroom where counsellor and student chat ,
    path('studentCounselling/', views.studentCounselling, name='studentCounselling'),
    # after student page, student will be directed here. if counsellor is free this will be skipped and student directly
    # goes to chatroom else gets notified that no counsellor is free,
    path('Recent/', views.Recent, name='Recent'),
    # this is to get the earliest unattended chatroom and get redirected to it.
    path('chatroom_refresh/<uuid:chatroom_id>', views.messagerefresh, name='chatroomrefresh'),
    # this is for json data of all msgs of any particular chatroom
    path('counsellor', views.counsellor_portal, name='counsellor'),
    # this is home page of counsellor.
    path('student', TemplateView.as_view(template_name='student.html'), name='student'),
    # button for student to proceed to studentCounselling page
    path('waiting_students', views.available_chatroom, name='waiting_students'),
    # to get json data of number of unattended chatrooms.
]
