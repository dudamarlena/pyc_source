# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/simplesite/lib/middleware.py
# Compiled at: 2008-11-07 12:07:58
import gzip, StringIO

class GzipMiddleware(object):

    def __init__(self, app, compresslevel=9):
        self.app = app
        self.compresslevel = compresslevel

    def __call__(self, environ, start_response):
        if 'gzip' not in environ.get('HTTP_ACCEPT_ENCODING', ''):
            return self.app(environ, start_response)
        if environ['PATH_INFO'][-3:] != '.js' and environ['PATH_INFO'][-4:] != '.css':
            return self.app(environ, start_response)
        buffer = StringIO.StringIO()
        output = gzip.GzipFile(mode='wb', compresslevel=self.compresslevel, fileobj=buffer)
        start_response_args = []

        def dummy_start_response(status, headers, exc_info=None):
            start_response_args.append(status)
            start_response_args.append(headers)
            start_response_args.append(exc_info)
            return output.write

        app_iter = self.app(environ, dummy_start_response)
        for line in app_iter:
            output.write(line)

        if hasattr(app_iter, 'close'):
            app_iter.close()
        output.close()
        buffer.seek(0)
        result = buffer.getvalue()
        headers = []
        for (name, value) in start_response_args[1]:
            if name.lower() != 'content-length':
                headers.append((name, value))

        headers.append(('Content-Length', str(len(result))))
        headers.append(('Content-Encoding', 'gzip'))
        start_response(start_response_args[0], headers, start_response_args[2])
        buffer.close()
        return [result]


def make_gzip_middleware(app, global_conf, **app_conf):
    compresslevel = int(app_conf.get('compresslevel', 9))
    return GzipMiddleware(app, compresslevel)


def make_gzip_middleware_filter(global_conf, **app_conf):
    compresslevel = int(app_conf.get('compresslevel', 9))

    def filter(app):
        return GzipMiddleware(app, compresslevel)

    return filter