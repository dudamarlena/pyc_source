# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/utils/profiler.py
# Compiled at: 2006-12-26 17:17:53
__doc__ = '\n    pocoo.utils.profiler\n    ~~~~~~~~~~~~~~~~~~~~\n\n    Provides a WSGI Profiler middleware for finding bottlenecks.\n\n    :license: GNU GPL, see LICENSE for more details.\n    :copyright: 2006 by Armin Ronacher.\n'
import sys
try:
    from cProfile import Profile
except ImportError:
    from profile import Profile

from pstats import Stats

class MergeStream(object):
    """
    A object that redirects `write` calls to multiple streams.
    Use this to log to both `sys.stdout` and a file::

        f = file('profiler.log')
        stream = MergeStream(sys.stdout, f)
        profiler = ProfilerMiddleware(app, stream)
    """
    __module__ = __name__

    def __init__(self, *streams):
        if not streams:
            raise TypeError('at least one stream must be given')
        self.streams = streams

    def write(self, data):
        for stream in self.streams:
            stream.write(data)


class ProfilerMiddleware(object):
    """
    Simple profiler middleware
    """
    __module__ = __name__

    def __init__(self, app, stream=sys.stdout):
        self._app = app
        self._stream = stream

    def __call__(self, environ, start_response):
        response_body = []

        def catching_start_response(status, headers, exc_info=None):
            start_response(status, headers, exc_info)
            return response_body.append

        def runapp():
            response_body.extend(self._app(environ, catching_start_response))

        p = Profile()
        p.runcall(runapp)
        body = ('').join(response_body)
        stats = Stats(p)
        stats.sort_stats('time', 'calls')
        self._stream.write('-' * 80)
        self._stream.write('\nPATH: %r\n' % environ.get('PATH_INFO'))
        stats.print_stats()
        self._stream.write('-' * 80 + '\n\n')
        return [
         body]