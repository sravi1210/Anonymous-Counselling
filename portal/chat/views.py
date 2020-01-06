from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect , HttpResponse
from django.shortcuts import render_to_response, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from chat import models
from .forms import Counsellorform
from .forms import Counselloreditform
from .forms import Message
from .models import messages,student,Chatroom,counsellor
from datetime import datetime
from django.urls import reverse


class SignUpView(CreateView):
    form_class = Counsellorform
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class Update(LoginRequiredMixin, CreateView):
    form_class = Counselloreditform
    success_url = reverse_lazy('home')
    template_name = 'update.html'


def Chat(request,chatroom_id):
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
            msg.message_time = datetime.now()
            msg.save()
            form = Message(instance=messages)
            m1 = chat[0].messages_set.all().filter(message_from=0)
            m2 = chat[0].messages_set.all().filter(message_from=1)

            return render(request, 'chat.html', context={'m1': m1, 'm2': m2, 'form': form}, )
        else:
            chat = Chatroom.objects.get(pk=chatroom_id)
            print(chat)
            print("HELLO")
            couns=chat.Counsellor
            chat.delete()
            couns.user_status = 0
            couns.save()
            return HttpResponseRedirect(reverse('home'))


    else:
        form = Message(instance=messages)
        args = {'form': form}
        return render(request, 'chat.html', args)

        

def studentCounselling(request):

    stud=student.objects.create()
    stud.student_status=True
    stud.save()
    chat = Chatroom.objects.create(start_time=datetime.now(),Student=stud)
    chat.save()
    for m in models.counsellor.objects.all():
        if m.user_status:
            return HttpResponseRedirect(reverse('chatroom', args=(chat.Chatroom_id,)))
    else:
        return HttpResponseRedirect(reverse('studentCounselling'))


def Recent(request):

    if request.user.is_authenticated:
        ac=Chatroom.objects.all().filter(active_status=0)

        if(ac.count!=0):    
            try:

                availablechatroom=ac[0]#0 or n-1 dekh lio
                couns=counsellor.objects.get(pk=request.user.id)
                availablechatroom.active_status=1
                availablechatroom.Counsellor=couns#pta ni shi hoga ya nhi
                chatroom_id=availablechatroom.Chatroom_id
                couns.user_status=1
                availablechatroom.save()
                couns.save()
                
                return HttpResponseRedirect(reverse('chatroom', args=(chatroom_id,)))
            except IndexError:
                return HttpResponse("There are no students right now")
        else:
            return HttpResponse("There are no students right now")
