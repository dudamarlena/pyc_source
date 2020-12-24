# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: M:\Programming\Project\django-auth\auth\CustomAuth\views\login.py
# Compiled at: 2019-12-21 15:55:52
# Size of source mod 2**32: 1356 bytes
from django.http import HttpRequest, HttpResponseRedirect
from CustomAuth.forms import UserLoginForm
import django.contrib.auth as user_login
from django.conf import settings
from django.shortcuts import render

def login(request: HttpRequest):
    if not request.user.is_anonymous:
        url = getattr(settings, 'USER_PROFILE_URL', '/profile/')
        return HttpResponseRedirect(url)
    if request.method == 'POST':
        form = UserLoginForm(data=(request.POST))
        if form.is_valid():
            form.clean()
            user_login(request, (form.get_user()), backend='django.contrib.auth.backends.ModelBackend')
            next_page = request.session.get('next', None)
            if next_page:
                url = next_page
            else:
                url = getattr(settings, 'USER_PROFILE_URL', '/profile/')
            return HttpResponseRedirect(url)
        context = {'errors':form.errors, 
         'form':UserLoginForm}
    else:
        context = {'form': UserLoginForm}
    if request.method == 'GET':
        next_page = request.GET.get('next', None)
        if next_page:
            request.session['next'] = next_page
    return render(request, 'CustomAuth/pages/login.html', context=context)