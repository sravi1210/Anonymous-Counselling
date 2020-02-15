import json
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from . import models
from .forms import Counsellorform
from .forms import Counselloreditform
from .forms import Message
from .models import messages, student, Chatroom, counsellor
from datetime import datetime
from django.urls import reverse
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt


class SignUpView(CreateView):
    form_class = Counsellorform
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class Update(LoginRequiredMixin, CreateView):
    form_class = Counselloreditform
    success_url = reverse_lazy('home')
    template_name = 'update.html'


def Chat(request, chatroom_id):
    try:
        t = models.Chatroom.objects.get(pk=chatroom_id)
    except ObjectDoesNotExist:
        if (request.user.is_authenticated):
            return HttpResponseRedirect(reverse('counsellor'))
        return HttpResponseRedirect(reverse('home'))
    if request.user.is_authenticated == 0:
        request.session.set_test_cookie()
        request.session['chatroom'] = Chatroom.objects.get(pk=chatroom_id).Student.id
        request.session['last_activity'] = datetime.now()
        request.session['chat'] = chatroom_id
    if request.method == 'POST':
        if 'chat' in request.POST:

            form = Message(request.POST)
            msg = form.save(commit=False)
            if models.counsellor.__instancecheck__(request.user):
                msg.message_from = 1
            else:
                msg.message_from = 0
            chat = Chatroom.objects.filter(pk=chatroom_id)
            msg.chat_session = chat[0]
            msg.message_time = now()
            msg.save()
            form = Message(instance=messages)
            m = chat[0].messages_set.all()

            return render(request, 'chat.html', context={'m': m, 'form': form, 'chatroomid': chatroom_id}, )
        else:
            stud = Chatroom.objects.get(pk=chatroom_id).Student
            stud.delete()
            if (request.user.is_authenticated):
                return HttpResponseRedirect(reverse('counsellor'))
            return HttpResponseRedirect(reverse('home'))


    else:
        form = Message(instance=messages)
        args = {'form': form}
        return render(request, 'chat.html', args)


def messagerefresh(request, chatroom_id):
    chat = Chatroom.objects.filter(pk=chatroom_id)
    m = chat[0].messages_set.all()
    m = serializers.serialize('json', m)
    return JsonResponse({'m': m, 'chatroomid': chatroom_id}, safe=False)


def studentCounselling(request):
    for m in models.counsellor.objects.all():
        if m.user_status == 1:
            stud = student.objects.create()
            stud.student_status = True
            stud.save()
            chat = Chatroom.objects.create(start_time=now(), Student=stud)
            chat.save()
            return HttpResponseRedirect(reverse('chatroom', args=(chat.Chatroom_id,)))
    return render(request, 'studentCounselling.html')


def Recent(request):
    if request.user.is_authenticated:
        ac = Chatroom.objects.all().filter(active_status=0)

        if (ac.count != 0):
            try:

                availablechatroom = ac[0]
                couns = counsellor.objects.get(pk=request.user.id)
                availablechatroom.active_status = 1
                availablechatroom.Counsellor = couns
                chatroom_id = availablechatroom.Chatroom_id
                availablechatroom.save()
                couns.save()

                return HttpResponseRedirect(reverse('chatroom', args=(chatroom_id,)))
            except IndexError:
                return HttpResponse("There are no students right now")
        else:
            return HttpResponse("There are no students right now")


def available_chatroom(request):
    if request.user.is_authenticated:
        data = Chatroom.objects.all().filter(active_status=0)
        data = serializers.serialize('json', data)
        return JsonResponse({'data': data})


def counsellor_portal(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            x = request.user
            if x.user_status == 0:
                x.user_status = 1
            else:
                x.user_status = 0
            x.save()
            return render(request, 'counsellor.html', context={'m': x.user_status, }, )
        else:
            return render(request, 'home.html')
    else:
        if request.user.is_authenticated:
            x = request.user
            x.user_status = 1
            x.save()
            return render(request, 'counsellor.html', context={'m': x.user_status, }, )
        else:
            return render(request, 'counsellor.html')
