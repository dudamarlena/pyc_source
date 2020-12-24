# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lxsameer/src/daarmaan/daarmaan/server/views/general.py
# Compiled at: 2012-09-16 08:38:20
import json
from django.shortcuts import render_to_response as rr
from django.shortcuts import redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from daarmaan.server.forms import PreRegistrationForm
from daarmaan.server.models import Profile, Service

@login_required
def dashboard(request):
    return HttpResponse()


@login_required
def setup_session(request):
    """
    Insert all needed values into user session.
    """
    return
    services = request.user.get_profile().services.all()
    services_id = [ i.id for i in services ]
    request.session['services'] = services_id


def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    remember = request.POST.get('remember_me', False)
    next_url = request.POST.get('next', None)
    form = PreRegistrationForm()
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            setup_session(request)
            if next_url:
                return HttpResponseRedirect('/')
            return redirect(reverse('dashboard-index', args=[]))
        else:
            return rr('index.html', {'regform': form, 'msgclass': 'error', 
               'next': next_url, 
               'msg': _('Your account is disabled.')}, context_instance=RequestContext(request))

    else:
        return rr('index.html', {'regform': form, 'msgclass': 'error', 
           'next': next_url, 
           'msg': _('Username or Password is invalid.')}, context_instance=RequestContext(request))
    return


def pre_register(request):
    return HttpResponse()


def index(request):
    """
    Main page.
    """
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('dashboard-index'))
    if request.method == 'POST':
        if request.POST['form'] == 'login':
            return login_view(request)
        else:
            return pre_register(request)

    else:
        form = PreRegistrationForm()
        next_url = request.GET.get('next', '')
        return rr('index.html', {'regform': form, 'next': next_url}, context_instance=RequestContext(request))