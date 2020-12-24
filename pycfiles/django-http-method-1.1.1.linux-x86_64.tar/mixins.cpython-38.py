# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.2/x64/lib/python3.8/site-packages/django_http_method/mixins.py
# Compiled at: 2020-05-04 11:30:43
# Size of source mod 2**32: 1290 bytes
import yaml
from urllib.parse import urlencode
from django.http import HttpResponseNotAllowed, QueryDict

class HttpMethodMixin:
    allowed = [
     'GET', 'POST', 'HEAD', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'TRACE']

    def dispatch(self, *args, **kwargs):
        if self.request.method == 'POST':
            data = self.request.POST
        else:
            if self.request.method == 'GET':
                data = self.request.GET
            else:
                if self.request.method in ('PATCH', 'PUT'):
                    data_dict = yaml.safe_load(self.request.body.decode())
                    data = QueryDict(urlencode(data_dict) if data_dict else {})
                else:
                    data = QueryDict()
        method = data.get('_method', self.request.method)
        if method:
            if method not in self.allowed:
                return HttpResponseNotAllowed(self.allowed, 'Method Not Allowed (' + method + ')')
            if '_method' in data:
                data._mutable = True
                del data['_method']
                data._mutable = False
            self.request.method = method
            self.request.META['REQUEST_METHOD'] = method
            setattr(self.request, method, data)
        return (super(HttpMethodMixin, self).dispatch)(*args, **kwargs)