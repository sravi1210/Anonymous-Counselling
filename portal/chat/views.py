from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from chat.models import counsellor
from .forms import Counsellorform
from .forms import Counselloreditform


class SignUpView(CreateView):
    form_class = Counsellorform
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class Update(LoginRequiredMixin, CreateView):
    form_class = Counselloreditform
    success_url = reverse_lazy('home')
    template_name = 'update.html'
