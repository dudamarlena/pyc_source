# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/frame/_response.py
# Compiled at: 2013-03-09 10:42:43
from dotdict import DotDict
from errors import Error404
from util import parse_query_string
import datetime
from _routes import routes
import os

class Response(object):

    def __init__(self, app, controller):
        if not controller:
            raise Error404
        self.app = app
        self.controller = controller
        self.headers = DotDict({'Content-Type': 'text/html', 
           'Cache-Control': 'no-store, no-cache, must-revalidate, max-age=0, post-check=0, pre-check=0', 
           'Pragma': 'no-cache'})
        self.status = '200 OK'
        self.additional_params = {}

    def set_cookie(self, key, value, expires=1, domain=None, path='/', secure=False, http_only=False):
        cookie = ['%s=%s' % (key, value)]
        if expires:
            now = datetime.datetime.utcnow()
            then = now + datetime.timedelta(hours=expires)
            cookie.append('Expires=%s' % then.strftime('%a, %d-%b-%Y %H:%M:%S UTC'))
        if domain:
            cookie.append('Domain=%s' % domain)
        if path:
            cookie.append('Path=%s' % path)
        if secure:
            cookie.append('Secure')
        if http_only:
            cookie.append('HttpOnly')
        self.headers['Set-Cookie'] = ('; ').join(cookie)

    def delete_cookie(self, key):
        self.headers['Set-Cookie'] = '%s=deleted; Expires=Thu, Jan 01 1970 00:00:00 GMT' % key

    def start_response(self):
        self._start_response(self.status, self.headers.items())

    def render(self, query_string, uri_data):
        params = parse_query_string(query_string)
        result = self.controller(**dict(params.items() + uri_data.items() + self.additional_params.items()))
        if result is None or isinstance(result, dict):
            method_name = self.controller.__name__
            if hasattr(self.controller.im_self, '__resource__'):
                template_dir = self.controller.im_self.__resource__['template_dir']
                template_path = os.path.join(template_dir, method_name + '.html')
                result = self.controller.im_self.get_template(template_path).render(result if result else {})
            else:
                template_dir = self.controller.im_self.__class__.__name__.lower()
                template_path = os.path.join(template_dir, method_name + '.html')
                result = self.controller.im_self.get_template(template_path).render(result if result else {})
        return result