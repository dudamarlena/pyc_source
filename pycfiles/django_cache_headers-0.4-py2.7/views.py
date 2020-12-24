# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cache_headers/tests/views.py
# Compiled at: 2017-11-17 03:42:00
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

def mylogin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponse('yay')
    else:
        raise RuntimeError('Bad credentials')
        return


def mylogout(request):
    logout(request)
    return HttpResponse('yay')