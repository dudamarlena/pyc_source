# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/prettydate/web.py
# Compiled at: 2009-01-21 16:49:15
"""
'prettyDate': a view with webob to display pretty dates
"""
from dateutil import parser
from paste.httpexceptions import HTTPExceptionHandler
from prettydate.pretty_date import prettyDate
from webob import Request, Response, exc

class View(object):
    defaults = {}

    def __init__(self, **kw):
        for key in self.defaults:
            setattr(self, key, kw.get(key, self.defaults[key]))

    def __call__(self, environ, start_response):
        request = Request(environ)
        date = request.params.get('date')
        if date is None:
            response = 'Please enter a date'
        else:
            try:
                date = parser.parse(date)
            except ValueError:
                response = 'Invalid date, "%s"' % date
                date = None

        if 'response' not in locals():
            response = prettyDate(date)
        return self.get_response(response)(environ, start_response)

    def get_response(self, text, content_type='text/plain'):
        """wrap a GET response"""
        res = Response(content_type=content_type, body=text)
        res.content_length = len(res.body)
        return res


def factory(global_conf, **app_conf):
    """create a webob view and wrap it in middleware"""
    key_str = 'prettyDate.'
    args = dict([ (key.split(key_str, 1)[(-1)], value) for (key, value) in app_conf.items() if key.startswith(keystr)
                ])
    app = View(**args)
    return HTTPExceptionHandler(app)