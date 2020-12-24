# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/dev/feedpubsub/waitressd/middleware.py
# Compiled at: 2018-03-01 15:30:54
# Size of source mod 2**32: 548 bytes
from logging import getLogger
import time
logger = getLogger('waitress.access')

def access_log(get_response):

    def middleware(request):
        start_time = time.monotonic()
        response = get_response(request)
        duration_ms = int((time.monotonic() - start_time) * 1000)
        logger.info('%d %s %s (%s %s) %d ms', response.status_code, request.method, request.get_full_path(), request.META['REMOTE_ADDR'], request.user, duration_ms)
        return response

    return middleware