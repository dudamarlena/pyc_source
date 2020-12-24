# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jonasbraun/Coding/iekadou/django-lare/django_lare/middlewares.py
# Compiled at: 2018-05-26 07:12:10
# Size of source mod 2**32: 602 bytes
from django_lare.models import Lare

class LareMiddleware(object):

    def process_request(self, request):
        request.lare = Lare(request)

    def process_response(self, request, response):
        if request.lare.is_enabled():
            response['X-LARE-VERSION'] = request.lare.version
        return response

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request=None):
        self.process_request(request)
        response = self.get_response(request)
        self.process_response(request, response)
        return response