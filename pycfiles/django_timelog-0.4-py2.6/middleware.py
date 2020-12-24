# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/timelog/middleware.py
# Compiled at: 2011-06-23 03:35:58
import time, logging
from django.utils.encoding import smart_str
logger = logging.getLogger(__name__)

class TimeLogMiddleware(object):

    def process_request(self, request):
        request._start = time.time()

    def process_response(self, request, response):
        if hasattr(request, '_start'):
            d = {'method': request.method, 'time': time.time() - request._start, 'code': response.status_code, 
               'url': smart_str(request.path_info)}
            msg = '%(method)s "%(url)s" (%(code)s) %(time).2f' % d
            logger.info(msg)
        return response