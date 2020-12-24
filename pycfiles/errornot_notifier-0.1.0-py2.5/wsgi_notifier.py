# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/errornot/wsgi_notifier.py
# Compiled at: 2010-03-09 05:34:03
from errornot import notifier
INTERESTING_ENV_INFOS = [
 'PATH_INFO',
 'SERVER_NAME',
 'SERVER_PORT',
 'HTTP_ACCEPT',
 'HTTP_ACCEPT_CHARSET',
 'HTTP_ACCEPT_ENCODING',
 'HTTP_ACCEPT_LANGUAGE',
 'HTTP_HOST',
 'REQUEST_METHOD',
 'REMOTE_ADDR']

class WSGINotifier(object):
    """WSGI Middleware standing on your middlewares stack and sending errors to ErrorNot.
  This middleware as to stand as low as possible in the middleware stack.
  It will except any exception, report it, and raise it back.
  """

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        try:
            for item in self.app(environ, start_response):
                yield item

        except:
            request, environment = {}, {}
            for name in INTERESTING_ENV_INFOS:
                environment[name] = environ.get(name)

            request['url'] = '%(wsgi.url_scheme)s://%(HTTP_HOST)s%(PATH_INFO)s?%(QUERY_STRING)s' % environ
            notifier.get_post_error(request, environment)
            raise