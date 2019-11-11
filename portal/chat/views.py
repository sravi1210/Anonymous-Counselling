from django.shortcuts import render
from django.http import HttpResponse
from .models import counsellor
# Create your views here.

def login(request):
    return render(request, 'chat/index.html')