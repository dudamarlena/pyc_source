# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/egonzalez/Development/django-requests-monitoring/monitoring/middleware.py
# Compiled at: 2018-06-14 04:56:22
# Size of source mod 2**32: 930 bytes
import time
from datadog import DogStatsd
from . import settings
from .statsd import StatsD
try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:

    class MiddlewareMixin(object):
        pass


statsd = StatsD(host=(settings.STATSD_HOST),
  port=(settings.STATSD_PORT),
  namespace=(settings.STATSD_PREFIX))

class RequestLatencyMiddleware(MiddlewareMixin):

    def process_request(self, request):
        request._begun_at = time.time()

    def process_response(self, request, response):
        if not hasattr(request, '_begun_at'):
            return response
        else:
            took_seconds = time.time() - request._begun_at
            statsd.client.histogram((settings.REQUEST_LATENCY_MIDDLEWARE_HIST),
              took_seconds,
              tags=(settings.REQUEST_LATENCY_MIDDLEWARE_TAGS + [
             'endpoint:{}'.format(request.path)]))
            return response