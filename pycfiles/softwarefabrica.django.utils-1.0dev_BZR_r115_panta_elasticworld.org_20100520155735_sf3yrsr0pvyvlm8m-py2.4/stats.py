# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/softwarefabrica/django/utils/middleware/stats.py
# Compiled at: 2009-11-11 07:07:52
"""
Performance statistics middleware

To use this middleware, in settings.py you need to set:

DEBUG_STATS   = True

MIDDLEWARE_CLASSES = (
    ...
    'softwarefabrica.django.utils.middleware.stats.StatsMiddleware',
    ...)
"""
import time
from operator import add
import re
from django.conf import settings
from django.db import connection

class StatsMiddleware(object):
    """
    Statistics middleware.
    """
    __module__ = __name__

    def process_view(self, request, view_func, view_args, view_kwargs):
        from django.conf import settings
        debug_stats = getattr(settings, 'DEBUG_STATS', False)
        if not debug_stats:
            return view_func(request, *view_args, **view_kwargs)
        debug = settings.DEBUG
        settings.DEBUG = True
        n = len(connection.queries)
        start = time.time()
        response = view_func(request, *view_args, **view_kwargs)
        totTime = time.time() - start
        queries = len(connection.queries) - n
        if queries:
            dbTime = reduce(add, [ float(q['time']) for q in connection.queries[n:] ])
        else:
            dbTime = 0.0
        pyTime = totTime - dbTime
        settings.DEBUG = debug
        stats = {'totTime': totTime, 'pyTime': pyTime, 'dbTime': dbTime, 'queries': queries}
        content_type = None
        if response.has_header('Content-Type'):
            content_type = response['Content-Type']
        if response and response.content and content_type.startswith('text/html'):
            s = response.content
            regexp = re.compile('(?P<cmt><!--\\s*STATS:(?P<fmt>.*?)-->)')
            match = regexp.search(s)
            if match:
                s = s[:match.start('cmt')] + match.group('fmt') % stats + s[match.end('cmt'):]
                response.content = s
        else:
            print stats
        return response