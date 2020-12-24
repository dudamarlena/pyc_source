# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/check_docking/middleware.py
# Compiled at: 2015-02-07 22:13:48
__doc__ = '检测中间件.'
__author__ = 'kylinfish@126.com'
__date__ = '2015/02/06'
from django import http
from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from check_docking.inspect import request_data_inspect

class InspectMiddleware(object):
    u"""检测请求参数的中间件, 在settings.py配置项MIDDLEWARE_CLASSES中增加.
    """

    def __init__(self):
        u"""要求务必是在调试模式下启用.
        """
        if not all((settings.DEBUG, getattr(settings, 'IS_DATA_INSPECT', None))):
            raise MiddlewareNotUsed
        return

    def process_view(self, request, view, args, kwargs):
        message = request_data_inspect(request)
        if message:
            response = http.HttpResponse(message)
            return response