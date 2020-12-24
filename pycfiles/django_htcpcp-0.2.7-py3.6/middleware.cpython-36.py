# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/djhtcpcp/middleware.py
# Compiled at: 2019-09-15 12:50:25
# Size of source mod 2**32: 875 bytes
from django.http import HttpResponse
try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

class HTCPCPMiddleware(MiddlewareMixin):
    coffee_list = [
     '/coffee/black/',
     '/coffee/espresso/']
    coffee_methods = [
     'BREW',
     'WHEN']

    def process_request(self, request):
        if request.path not in self.coffee_list:
            if request.method not in self.coffee_methods:
                return
            else:
                if request.path not in self.coffee_list:
                    return HttpResponse("I'm a teapot.", status=418)
                if request.path in self.coffee_list:
                    if request.method == 'BREW':
                        return HttpResponse('Say WHEN . . . ', status=100)
        else:
            if request.path in self.coffee_list:
                if request.method == 'WHEN':
                    return HttpResponse('Mmmmmmm coffee!', status=201)