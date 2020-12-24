# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/web/frontend/debug/debug_resolved_email.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
from sentry.models import Activity
from .mail import ActivityMailDebugView

class DebugResolvedEmailView(ActivityMailDebugView):

    def get_activity(self, request, event):
        return {'type': Activity.SET_RESOLVED}