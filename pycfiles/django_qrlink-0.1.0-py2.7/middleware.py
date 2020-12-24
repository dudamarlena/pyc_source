# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/qrlink/middleware.py
# Compiled at: 2011-02-15 04:41:18
from django.conf import settings
from django.contrib.sites.models import Site
from django.db import DatabaseError
import re

class QrlinkMiddleware(object):
    try:
        site = Site.objects.get_current()
    except (DatabaseError, Site.DoesNotExist):
        site = None

    chart = 'http://chart.apis.google.com/chart?chs=100x100&cht=qr&chl='

    def __init__(self):
        pass

    def qrlink(self, request):
        if not self.site:
            base_path = 'http://%s:%s' % (
             request.META['SERVER_NAME'], request.META['SERVER_PORT'])
        else:
            base_path = site.domain
        return '%s%s%s' % (self.chart, base_path, request.path)

    def process_response(self, request, response):
        response.content = re.sub('(</body>)', '<img src="%s" />\\1' % self.qrlink(request), response.content)
        return response