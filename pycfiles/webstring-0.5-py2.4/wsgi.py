# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\webstring\wsgi.py
# Compiled at: 2007-01-03 20:14:19
"""WSGI middleware base class."""
__all__ = [
 'WSGIBase']

class WSGIBase(object):
    """Base class for WSGI middleware."""
    __module__ = __name__

    def __init__(self, application, source, **kw):
        """Initializes the class.

        @param application The WSGI application using this class must return a
        tuple or dictionary for its iterable and, at minimum, create an entry
        in the "environ" dictionary for a valid source template under the key
        "webstring.source". Other entries can be set as needed.

        Simple example:

        @template('template.html')
        def simple_app(environ, start_response):
        ... status = '200 OK'
        ... response_headers = [('Content-type','text/html')]
        ... start_response(status, response_headers)
        ... return {'test':'Hello world!
'}        
        """
        self.application = application
        auto, mx = kw.get('auto', True), kw.get('max', 25)
        temps, eng = kw.get('templates'), kw.get('engine', 'etree')
        self.encoding = kw.get('encoding', 'utf-8')
        self.format = kw.get('format', self._format)
        self.template = self._klass(source, auto, mx, format=self._format, engine=eng, templates=temps)

    def __call__(self, environ, start_response):
        result = self.application(environ, start_response)
        return [str(self.template.render(result, self.format, self.encoding))]