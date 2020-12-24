# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: M:\Programming\Project\django-auth\auth\CustomAuth\views\verfiy_user.py
# Compiled at: 2020-01-28 13:32:35
# Size of source mod 2**32: 1001 bytes
from CustomAuth.models import User
from CustomAuth.tokens import account_verify_email_token
from django.contrib.auth import login
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.conf import settings

def verify_code(request, verify_uid64, token):
    try:
        uid = force_text(urlsafe_base64_decode(verify_uid64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None:
        if account_verify_email_token.check_token(user, token):
            user.is_verify = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return HttpResponseRedirect(getattr(settings, 'VERIFY_SUCCESSFULLY', '/profile/'))
    return HttpResponse(getattr(settings, 'VERIFY_FAILED', 'Verification link is invalid!'))