# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: M:\Programming\Project\django-auth\auth\CustomAuth\views\resend_verification_code.py
# Compiled at: 2020-01-28 13:32:35
# Size of source mod 2**32: 568 bytes
from django.http import HttpRequest
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from CustomAuth.models import User

@login_required(login_url='/login/')
def resend_verification_code(request: HttpRequest):
    user = request.user
    context = {}
    if not user.is_verify:
        user.send_verification_code(request)
    else:
        context = {'user_already_verified': True}
    return render(request, 'CustomAuth/pages/resend_verification_code.html', context=context)