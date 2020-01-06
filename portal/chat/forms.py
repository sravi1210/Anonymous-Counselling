from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import counsellor, messages


class Counsellorform(UserCreationForm):
    class Meta:
        model = counsellor
        fields = ('username', 'user_information', 'password')


class Counselloreditform(UserChangeForm):
    class Meta:
        model = counsellor
        fields = ('user_information', 'email')


class Message(ModelForm):
    class Meta:
        model = messages
        fields = ('message',)
