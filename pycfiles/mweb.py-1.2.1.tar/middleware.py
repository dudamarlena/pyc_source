# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\Project\webapp\test\middleware.py
# Compiled at: 2018-01-21 05:55:38
from mwebapp.webapp import ctx

class PathAutoCompleter(object):

    def __init__(self, app):
        self.app = app

    def __call__(self, *args, **kwargs):
        request = ctx.request
        path = request.path_info
        if not path.endswith('/') and not path.startswith('/static'):
            request.path_info = path + '/'
        return self.app()