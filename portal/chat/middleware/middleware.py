from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
import datetime
from django.urls import reverse_lazy, reverse
from .. import models
from django.utils.deprecation import MiddlewareMixin
from datetime import datetime
from django.http import HttpResponseRedirect


class SessionExpiredMiddleware(MiddlewareMixin):
    def process_request(self, request):
        now = datetime.now()
        if request.user.is_authenticated == 0:
            if request.session.has_key('last_activity') and request.session.has_key('chatroom') and (
                    now - request.session['last_activity']).seconds > 600:
                try:
                    stud = models.student.objects.get(pk=request.session['chatroom'])
                    stud.delete()
                    del request.session
                    messages.add_message(request, messages.ERROR, 'Your session has been timed out.')
                    return HttpResponseRedirect(reverse('home'))
                except ObjectDoesNotExist:
                    messages.add_message(request, messages.ERROR, 'Your session has been timed out.')
        return None
