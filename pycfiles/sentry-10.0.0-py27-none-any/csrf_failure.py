# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/web/frontend/csrf_failure.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
from django.middleware.csrf import REASON_NO_REFERER
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.utils.decorators import method_decorator
from sentry.web.helpers import render_to_response

class CsrfFailureView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, reason=''):
        context = {'no_referer': reason == REASON_NO_REFERER, 'request': request}
        return render_to_response('sentry/403-csrf-failure.html', context, request, status=403)


view = CsrfFailureView.as_view()