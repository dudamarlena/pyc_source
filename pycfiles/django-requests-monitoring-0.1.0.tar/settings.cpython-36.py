# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/egonzalez/EricssonGitLab/clients/mediafirst-analytics-backend/ivibackend/monitoring/settings.py
# Compiled at: 2018-06-14 04:08:25
# Size of source mod 2**32: 471 bytes
from django.conf import settings
STATSD_HOST = getattr(settings, 'STATSD_HOST', '0.0.0.0')
STATSD_PORT = getattr(settings, 'STATSD_PORT', 9125)
STATSD_PREFIX = getattr(settings, 'STATSD_PREFIX', None)
STATSD_MAXUDPSIZE = getattr(settings, 'STATSD_MAXUDPSIZE', 512)
REQUEST_LATENCY_MIDDLEWARE_HIST = getattr(settings, 'REQUEST_LATENCY_MIDDLEWARE_HIST', 'request.duration.seconds')
REQUEST_LATENCY_MIDDLEWARE_TAGS = getattr(settings, 'REQUEST_LATENCY_MIDDLEWARE_TAGS', [])