# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/brightcontent/core/renderer.py
# Compiled at: 2006-09-01 03:06:21
from Ft.Xml.Xslt import Transform
from brightcontent.util import get_base_url
XSL = 'brightcontent/static/bluesky/index.xslt'
BC_NS = 'http://brightcontent.net/ns/'

class FeedRenderer(object):
    __module__ = __name__

    def __init__(self, application):
        self.application = application

    def start_response(self, status, headers, exc_info=None):
        self.status = status
        self.headers = headers
        self.exc_info = exc_info

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        cache = environ['beaker.cache'].get_cache('brightcontent')
        try:
            result = cache.get_value(path)
        except:
            result = self.application(environ, self.start_response)
            if environ.get('brightcontent.render', False):
                self.headers = [('Content-type', 'text/html')]
                params = dict([ ((BC_NS, k), environ[k]) for k in environ ])
                params[(BC_NS, 'weblog-base-uri')] = get_base_url(environ)
                result = Transform(('').join(result[0]), XSL, params=params)
            if isinstance(result, str):
                result = [
                 result]
            cache.set_value(path, result)

        start_response(self.status, self.headers, self.exc_info)
        return result