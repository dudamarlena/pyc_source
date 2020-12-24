# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/django_includes/middleware.py
# Compiled at: 2020-01-02 03:06:44
# Size of source mod 2**32: 1306 bytes
import re
from http.cookiejar import split_header_words
import requests
esi_include_re = re.compile(b'<esi:include src="([^"]+)" />')

class EdgeSideIncludesMiddleware(object):
    __doc__ = '\n    This middleware is intended to resolve edge side includes, as would do a system side middleware like Varnish. It is\n    by no mean complete, efficient or secure, please consider using a real implementation if running in production.\n\n    Please note that this is a WSGI middleware, and not a django middleware. Use it by patching your wsgi.py file to\n    decorate the django application.\n\n    '

    def __init__(self, application, session=None):
        self.application = application
        self.environ = None
        self.session = session or requests.Session()

    def include(self, match):
        cookies = self.environ.get('HTTP_COOKIE', '') or None
        if cookies:
            cookies = dict(split_header_words([cookies])[0])
        response = self.session.get(match.group(1), cookies=cookies)
        return response.content

    def __call__(self, environ, start_response):
        self.environ = environ
        for x in self.application(environ, start_response):
            yield esi_include_re.sub(self.include, x)