from django.contrib import admin
from django.urls import path, include
from . import views
from . import views

app_name = "chat"
urlpatterns = [
    path('login/',views.login),
]