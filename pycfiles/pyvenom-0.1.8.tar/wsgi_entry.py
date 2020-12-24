# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Larco/Documents/Github/pyvenom/framework/venom/wsgi_entry.py
# Compiled at: 2016-04-12 00:09:11
__all__ = [
 'WSGIEntryPoint']
import webapp2

class WSGIEntryPoint(object):
    allowed_methods = frozenset(('GET', 'POST', 'PUT', 'PATCH', 'HEAD', 'DELETE', 'OPTIONS',
                                 'TRACE'))

    def __init__(self):
        self._form_request_handler()
        self.wsgi = webapp2.WSGIApplication([('.*', self._entrypoint)], debug=False)
        self.wsgi.allowed_methods = self.allowed_methods

    def dispatch(self, request, response, error):
        raise NotImplementedError()

    def _form_request_handler(self):
        wsgientry = self

        class MainHandler(webapp2.RequestHandler):

            def dispatch(self):
                new_wsgi = wsgientry.dispatch(self.request, self.response, self.error)
                if isinstance(new_wsgi, WSGIEntryPoint):
                    return new_wsgi

        self._entrypoint = MainHandler

    def __call__(self, *args, **kwargs):
        return self.wsgi(*args, **kwargs)