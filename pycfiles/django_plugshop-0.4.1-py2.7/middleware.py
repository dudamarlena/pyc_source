# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/plugshop/middleware.py
# Compiled at: 2014-08-09 03:47:51
from plugshop import settings
from plugshop.cart import Cart

class CartMiddleware(object):

    def process_request(self, request):
        setattr(request, settings.REQUEST_NAMESPACE, Cart(request, settings.SESSION_NAMESPACE))

    def process_response(self, request, response):
        if hasattr(request, settings.REQUEST_NAMESPACE):
            cart = getattr(request, settings.REQUEST_NAMESPACE)
            cart.save()
        return response