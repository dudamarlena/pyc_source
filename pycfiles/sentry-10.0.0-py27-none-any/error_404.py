# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/web/frontend/error_404.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
from django.views.generic import View
from django.template import Context, loader
from django.http import HttpResponseNotFound

class Error404View(View):

    def dispatch(self, request):
        context = {'request': request}
        t = loader.get_template('sentry/404.html')
        return HttpResponseNotFound(t.render(Context(context)))