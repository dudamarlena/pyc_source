# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/harold/sessions/mpsession.py
# Compiled at: 2006-08-02 05:57:51
from harold.lib.mpwsgi import apache_request_key
from mod_python import apache, Session
from paste.wsgilib import add_close
apache_session_key = 'apache.session.factory'

class HeaderCatcher(object):
    __module__ = __name__

    def __init__(self, request, wsgi_headers):
        self.request = request
        self.wsgi_headers = wsgi_headers

    def headers_out(self):
        return self.wsgi_headers

    headers_out = property(headers_out)

    def __getattr__(self, name):
        return getattr(self.request, name)


class ApacheSessionMiddleware:
    __module__ = __name__

    def __init__(self, app, **kwds):
        self.app = app
        self.kwds = kwds

    def __call__(self, environ, start_response):
        output_headers = apache.table()

        def factory():
            req = HeaderCatcher(environ[apache_request_key], output_headers)
            sid = self.sid()
            secret = self.secret()
            session = self.session = Session.Session(req, sid, secret)
            return session

        environ[apache_session_key] = factory

        def session_start_response(status, headers, exc_info=None):
            headers.extend(output_headers.items())
            return start_response(status, headers, exc_info)

        return add_close(self.app(environ, session_start_response), self.close)

    def sid(self):
        try:
            return self.kwds['sid']
        except (KeyError,):
            return 0

    def secret(self):
        try:
            return self.kwds['secret']
        except (KeyError,):
            return 'always ask for 10% discount on purchase price'

    def close(self):
        try:
            self.session.save()
        except (AttributeError,):
            pass