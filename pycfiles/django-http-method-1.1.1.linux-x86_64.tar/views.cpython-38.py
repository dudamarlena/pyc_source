# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.2/x64/lib/python3.8/site-packages/django_http_method/views.py
# Compiled at: 2020-05-04 11:30:43
# Size of source mod 2**32: 1572 bytes
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from .mixins import HttpMethodMixin

class TestView(HttpMethodMixin, View):
    template_name = 'django_http_method_mixins/template.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, {'method':'Received a GET', 
         'params':self.request.GET.dict()})

    def post(self, *args, **kwargs):
        return render(self.request, self.template_name, {'method':'Received a POST', 
         'params':self.request.POST.dict()})

    def head(self, *args, **kwargs):
        return render(self.request, self.template_name, {'method': 'Received a HEAD'})

    def put(self, *args, **kwargs):
        return render(self.request, self.template_name, {'method':'Received a PUT', 
         'params':self.request.PUT.dict()})

    def delete(self, *args, **kwargs):
        return render(self.request, self.template_name, {'method': 'Received a DELETE'})

    def patch(self, *args, **kwargs):
        return render(self.request, self.template_name, {'method':'Received a PATCH', 
         'params':self.request.PATCH.dict()})

    def options(self, *args, **kwargs):
        return render(self.request, self.template_name, {'method': 'Received a OPTIONS'})

    def trace(self, *args, **kwargs):
        return render(self.request, self.template_name, {'method': 'Received a TRACE'})