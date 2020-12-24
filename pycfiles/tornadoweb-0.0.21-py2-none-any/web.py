# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /app/insight2/tornadoweb/web.py
# Compiled at: 2019-09-24 23:19:41
from inspect import isclass
from tornado.web import RequestHandler, ErrorHandler

class BaseHandler(RequestHandler):
    """
        Torando RequestHandler
        http://www.tornadoweb.org/

    """
    __UID__ = '__UID__'
    __USERNAME__ = '__USERNAME__'

    def get(self, *args, **kwargs):
        self.send_error(404)

    def post(self, *args, **kwargs):
        self.send_error(404)

    def get_current_user(self):
        return self.get_secure_cookie(self.__USERNAME__)


ErrorHandler.__bases__ = (
 BaseHandler,)

def url(pattern, order=0):

    def actual(handler):
        if not isclass(handler) or not issubclass(handler, RequestHandler):
            raise Exception("must be RequestHandler's sub class.")
        if not hasattr(handler, '__urls__'):
            handler.__urls__ = []
        handler.__urls__.append((pattern, order))
        return handler

    return actual


__all__ = [
 'BaseHandler', 'url']