# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\wsgiserialize\json.py
# Compiled at: 2006-12-16 12:18:37
import simplejson
__all__ = [
 'WSGIJson', 'jsonize']

def jsonize(application):
    """Decorator for JSON serialization."""
    return WSGIJson(application)


class WSGIJson(object):
    """WSGI middleware for serializing simple Python objects to JSON."""
    __module__ = __name__

    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        """Serializes simple Python objects to JSON."""
        return [
         simplejson.dumps(self.application(environ, start_response))]