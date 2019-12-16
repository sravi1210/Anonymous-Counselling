from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import Counsellorform, Counselloreditform
from .models import counsellor, student, Chatroom, messages

admin.site.register(counsellor)
admin.site.register(student)
admin.site.register(messages)
admin.site.register(Chatroom)


class CustomUserAdmin(UserAdmin):
    add_form = Counsellorform
    form = Counselloreditform
    model = counsellor
    list_display = ['username']
