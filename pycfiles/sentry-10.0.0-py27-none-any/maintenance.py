# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/middleware/maintenance.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import, print_function
import logging
from django.conf import settings
from django.http import HttpResponse
logger = logging.getLogger('sentry.errors')
DB_ERRORS = []
try:
    import psycopg2
except ImportError:
    pass
else:
    DB_ERRORS.append(psycopg2.OperationalError)

DB_ERRORS = tuple(DB_ERRORS)

class ServicesUnavailableMiddleware(object):

    def process_request(self, request):
        if settings.MAINTENANCE:
            return HttpResponse('Sentry is currently in maintenance mode', status=503)

    def process_exception(self, request, exception):
        if isinstance(exception, DB_ERRORS):
            logger.exception('Fatal error returned from database')
            return HttpResponse('Sentry is currently in maintenance mode', status=503)