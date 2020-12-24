# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/web/frontend/auth_close.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
from django.shortcuts import render_to_response
from sentry.web.frontend.base import BaseView

class AuthCloseView(BaseView):
    """This is a view to handle when sentry log in has been opened from
    another window. This view loads an html page with a script that sends a message
    back to the window opener and closes the window"""

    def handle(self, request):
        logged_in = request.user.is_authenticated()
        return render_to_response('sentry/auth_close.html', {'logged_in': logged_in})