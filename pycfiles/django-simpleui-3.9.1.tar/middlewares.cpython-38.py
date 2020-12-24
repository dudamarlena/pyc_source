# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/panjing/dev/simplepro_demo/simpleui/middlewares.py
# Compiled at: 2019-12-08 23:37:24
# Size of source mod 2**32: 341 bytes
import os
try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object
else:

    class SimpleMiddleware(MiddlewareMixin):

        def process_response(self, request, response):
            response['X-Frame-Options'] = 'ALLOW-FROM'
            return response