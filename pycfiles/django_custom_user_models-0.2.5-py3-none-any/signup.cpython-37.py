# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: M:\Programming\Project\django-auth\auth\CustomAuth\views\signup.py
# Compiled at: 2020-01-28 13:32:35
# Size of source mod 2**32: 979 bytes
from django.http import HttpRequest, HttpResponseRedirect
from CustomAuth.forms import UserCreationForm
from django.contrib.auth import login
from django.conf import settings
from django.shortcuts import render

def signup(request: HttpRequest):
    if request.method == 'POST':
        form = UserCreationForm(data=(request.POST))
        if form.is_valid():
            if form.clean_password2():
                user = form.save()
                user.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                user.send_verification_code(request)
                return HttpResponseRedirect(getattr(settings, 'SIGNUP_SUCCESSFULLY_URL', '/profile/'))
        context = {'errors':form.errors,  'form':UserCreationForm}
    else:
        context = {'form': UserCreationForm}
    return render(request, 'CustomAuth/pages/signup.html', context)