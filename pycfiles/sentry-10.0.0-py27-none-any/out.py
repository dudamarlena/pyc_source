# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/web/frontend/out.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
from django.conf import settings
from django.http import Http404, HttpResponseRedirect
from django.views.generic import View
from sentry import options

class OutView(View):

    def get(self, request):
        if not settings.SENTRY_ONPREMISE:
            raise Http404
        install_id = options.get('sentry:install-id')
        if install_id:
            query = '?install_id=' + install_id
        else:
            query = ''
        return HttpResponseRedirect('https://sentry.io/from/self-hosted/' + query)