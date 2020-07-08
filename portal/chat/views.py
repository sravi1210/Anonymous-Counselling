from django.core import serializers
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.urls import reverse_lazy
from django.utils.timezone import now
from django.views.generic.edit import CreateView

from . import models
from .forms import Counselloreditform
from .forms import Message
from .models import messages, student, Chatroom, counsellor
import datetime

from datetime import datetime, timezone
from apscheduler.schedulers.background import BackgroundScheduler
from django.http import HttpResponse
from django.shortcuts import redirect


def m():
    chats = Chatroom.objects.all()
    for chat in chats:
        msgs = chat.messages_set.all()
        t = now()
        min_time = 9000000
        for msg in msgs:
            if (t - msg.message_time).seconds < min_time and msg.message_from is False:
                min_time = (t - msg.message_time).seconds
        print(chat.Chatroom_id)
        if min_time > 600:
            stu = chat.Student
            print(stu)
            stu.delete()
    print("done")


def ask():
    scheduler = BackgroundScheduler()
    scheduler.add_job(m, 'interval', seconds=3600)
    scheduler.start()


class Update(LoginRequiredMixin, CreateView):
    form_class = Counselloreditform
    success_url = reverse_lazy('home')
    template_name = 'update.html'


def Chat(request, chatroom_id):
    try:
        t = models.Chatroom.objects.get(pk=chatroom_id)
    except ObjectDoesNotExist:
        # if chatroom does not exist or anyone tries to be smart
        if request.user.is_authenticated:
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
            # to check if request.user is an instance of the counsellor model.
            if models.counsellor.__instancecheck__(request.user):
                msg.message_from = 1
            else:
                msg.message_from = 0
            chat = Chatroom.objects.filter(pk=chatroom_id)
            msg.chat_session = chat[0]
            msg.message_time = datetime.now()
            msg.save()
            form = Message(instance=messages)
            # _set.all() gives all messages whose foreign key is given chatroom
            m = chat[0].messages_set.all()
            return render(request, 'chat.html', context={'m': m, 'form': form, 'chatroomid': chatroom_id}, )
        else:
            # this is when student anyone clicks cross this will delete student so by foreign key chatroom so msgs
            stud = Chatroom.objects.get(pk=chatroom_id).Student
            stud.delete()
            if request.user.is_authenticated:
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
            message = messages.objects.create(chat_session=chat,
                                              message="Hi, our anonymous user."
                                                      "Please wait till counsellor joins the discussion",
                                              message_time=now())
            message.save()
            return HttpResponseRedirect(reverse('chatroom', args=(chat.Chatroom_id,)))
    return render(request, 'studentCounselling.html')


def Recent(request):
    if request.user.is_authenticated:
        ac = Chatroom.objects.all().filter(active_status=0)

        if ac.count != 0:
            try:

                availablechatroom = ac[0]
                couns = counsellor.objects.get(pk=request.user.id)
                availablechatroom.active_status = 1
                availablechatroom.Counsellor = couns
                chatroom_id = availablechatroom.Chatroom_id
                availablechatroom.save()
                couns.save()
                message = messages.objects.create(chat_session=availablechatroom,
                                                  message="Hi, I am the counsellor.Let's talk.",
                                                  message_time=now(), message_from=True)
                message.save()
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
