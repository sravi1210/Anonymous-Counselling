from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import counsellor


class Counsellorform(UserCreationForm):
    class Meta:
        model = counsellor
        fields = ('user_name', 'user_information')


class Counselloreditform(UserChangeForm):
    class Meta:
        model = counsellor
        fields = ('user_name', 'user_information')
