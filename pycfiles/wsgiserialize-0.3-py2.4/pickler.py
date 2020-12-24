# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\wsgiserialize\pickler.py
# Compiled at: 2006-12-06 22:56:10
import pickle
__all__ = [
 'WSGIPickle', 'pickler']

def pickler(application):
    """Decorator for pickle serialization."""
    return WSGIPickle(application)


class WSGIPickle(object):
    """WSGI middleware for serializing simple Python objects with pickle."""
    __module__ = __name__

    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        """Serializes simple Python objects with pickle."""
        return [
         pickle.dumps(self.application(environ, start_response))]