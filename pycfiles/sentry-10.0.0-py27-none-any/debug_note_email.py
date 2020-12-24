# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/web/frontend/debug/debug_note_email.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
from sentry.models import Activity
from .mail import ActivityMailDebugView, get_random, make_message

class DebugNoteEmailView(ActivityMailDebugView):

    def get_activity(self, request, event):
        random = get_random(request)
        return {'type': Activity.NOTE, 
           'user': request.user, 
           'data': {'text': make_message(random, max(2, int(random.weibullvariate(12, 0.4))))}}