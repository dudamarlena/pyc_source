# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\yuuta\YCU-Programing\Code_Review\ura_1\django_press\middleware\rendering.py
# Compiled at: 2019-12-20 02:49:33
# Size of source mod 2**32: 590 bytes
from django.http import HttpRequest
from django.template.response import TemplateResponse
from django_press.models import Context

class RenderingMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    @staticmethod
    def process_template_response(request: HttpRequest, response: TemplateResponse):
        response.context_data.update(dict(core=(dict(Context.objects.values_list('key', 'value')))))
        return response