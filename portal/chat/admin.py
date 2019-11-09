from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import Counsellorform, Counselloreditform
from .models import counsellor, student, Chatroom, messages

admin.site.register(counsellor, student)


class CustomUserAdmin(UserAdmin):
    add_form = Counsellorform
    form = Counselloreditform
    model = counsellor
    list_display = ['user_name']
