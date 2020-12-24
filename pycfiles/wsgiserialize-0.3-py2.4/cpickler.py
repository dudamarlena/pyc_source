# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\wsgiserialize\cpickler.py
# Compiled at: 2006-12-06 22:56:10
import cPickle
__all__ = [
 'WSGICpickle', 'cpickler']

def cpickler(application):
    """Decorator for cPickle serialization."""
    return WSGICpickle(application)


class WSGICpickle(object):
    """WSGI middleware for serializing simple Python objects with cPickle."""
    __module__ = __name__

    def __init__(self, application):
        self.application = application

    def __call__(self, environ, start_response):
        """Serializes simple Python objects with cPickle."""
        return [
         cPickle.dumps(self.application(environ, start_response))]