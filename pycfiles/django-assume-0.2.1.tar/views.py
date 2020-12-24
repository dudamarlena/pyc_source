# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bryan/.virtualenvs/brainmaven3/lib/python2.6/site-packages/assume/views.py
# Compiled at: 2011-09-03 17:08:28
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, SESSION_KEY, BACKEND_SESSION_KEY
from django.contrib.auth.models import User
from django.contrib import messages
CAN_ASSUME_STAFF = getattr(settings, 'CAN_ASSUME_STAFF', False)
URL_AFTER_ASSUME = getattr(settings, 'URL_AFTER_ASSUME', '/')

@staff_member_required
def assume_user(request, id, next_url=URL_AFTER_ASSUME):
    """
    Custom admin view that logs into a specified user account.
    """
    user = get_object_or_404(User, pk=id)
    if user.is_staff and not CAN_ASSUME_STAFF:
        messages.error(request, 'Sorry, staff members cannot be assumed.')
        return HttpResponseRedirect(reverse('admin:auth_user_change', args=(user.id,)))
    user = authenticate(username=user.username)
    if SESSION_KEY in request.session:
        if request.session[SESSION_KEY] != user.id:
            request.session.flush()
    else:
        request.session.cycle_key()
    request.session[SESSION_KEY] = user.id
    request.session[BACKEND_SESSION_KEY] = user.backend
    if hasattr(request, 'user'):
        request.user = user
    return HttpResponseRedirect(next_url)