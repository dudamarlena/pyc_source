# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/plugins/base/response.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
__all__ = ('Response', 'JSONResponse')
from django.core.context_processors import csrf
from django.http import HttpResponse
from sentry.utils import json

class Response(object):

    def __init__(self, template, context=None):
        self.template = template
        self.context = context

    def respond(self, request, context=None):
        return HttpResponse(self.render(request, context))

    def render(self, request, context=None):
        from sentry.web.helpers import render_to_string
        if not context:
            context = {}
        if self.context:
            context.update(self.context)
        context.update(csrf(request))
        return render_to_string(self.template, context, request)


class JSONResponse(Response):

    def __init__(self, context, status=200):
        self.context = context
        self.status = status

    def respond(self, request, context=None):
        return HttpResponse(json.dumps(self.context), content_type='application/json', status=self.status)