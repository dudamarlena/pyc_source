# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\wsgiserialize\yamlize.py
# Compiled at: 2006-12-16 12:39:14
import yaml
__all__ = [
 'WSGIYaml', 'yamlize']

def yamlize(application):
    """Decorator for YaML serialization.

    @param application WSGI application.
    """
    return WSGIYaml(application)


class WSGIYaml(object):
    """WSGI middleware for serializing simple Python objects to YaML."""
    __module__ = __name__

    def __init__(self, application):
        """Initializes the class.

        @param application WSGI application.
        """
        self.application = application

    def __call__(self, environ, start_response):
        """Serializes simple Python objects to YaML."""
        return [
         yaml.dump(self.application(environ, start_response))]