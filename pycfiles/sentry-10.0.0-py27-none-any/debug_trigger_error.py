# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/web/frontend/debug/debug_trigger_error.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
from django.views.generic import View
from sentry.web.frontend.error_500 import Error500View
from sentry.utils.sdk import capture_exception

class DebugTriggerErrorView(View):

    def get(self, request):
        try:
            raise ValueError('An example error')
        except Exception:
            capture_exception()

        return Error500View.as_view()(request)