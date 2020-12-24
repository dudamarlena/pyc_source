# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cox/Documents/GitHub/GoogleAuthenticatorPyPI/django_google_auth2/google/bindgoogleauth/bindgoogleauthapi.py
# Compiled at: 2019-04-02 07:05:00
# Size of source mod 2**32: 424 bytes
from django.shortcuts import render, HttpResponse
from django_google_auth2.google.bindgoogleauth.bindgoogleauth import bind_google_auth
import json

def bind_google_auth_api(request):
    body = json.loads(request.body)
    data = bind_google_auth(body['user'])
    status = data['success']
    if not status:
        return HttpResponse(data['data'])
    else:
        return render(request, 'google.html', {'qr_code': data['data']})