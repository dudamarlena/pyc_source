# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/dev/signalbox/signalbox/middleware/loginformmiddleware.py
# Compiled at: 2014-08-27 19:26:12
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login

class LoginFormMiddleware(object):

    def process_request(self, request):
        if request.method == 'POST' and 'is_top_login_form' in request.POST:
            form = AuthenticationForm(data=request.POST)
            if form.is_valid():
                login(request, form.get_user())
                if '/account/logout/' in request.get_full_path():
                    return HttpResponseRedirect('/')
        else:
            form = AuthenticationForm(request)
        request.login_form = form