from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from chat import models
from .forms import Counsellorform
from .forms import Counselloreditform
from .forms import Message
from .models import messages


class SignUpView(CreateView):
    form_class = Counsellorform
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class Update(LoginRequiredMixin, CreateView):
    form_class = Counselloreditform
    success_url = reverse_lazy('home')
    template_name = 'update.html'


def Chat(request, p):
    if request.method == 'POST':
        form = Message(request.POST)
        form.messages.message_from = p
        m1 = messages.objects.all().filter(message_from=1).sort(key=messages.message_time)[:10]
        m2 = messages.objects.all().filter(message_from=0).sort(key=messages.message_time)[:10]
        if form.is_valid():
            return render(request, 'chat.html', context={'m1': m1, 'm2': m2})
