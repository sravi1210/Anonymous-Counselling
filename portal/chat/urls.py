from django.contrib import admin
from django.urls import path, include
from . import views
from .models import counsellor
from django.views.generic.base import TemplateView

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('update/', views.Update.as_view(), name='update'),
]
