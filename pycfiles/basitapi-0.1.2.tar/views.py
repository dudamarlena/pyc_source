# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/omer/Projects/DjangoProjects/basitapi/basitapi/views.py
# Compiled at: 2013-04-25 14:09:46
import django
from django.utils import simplejson
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, QueryDict
from basitapi.exception import ApiException
from basitapi.response import ApiResponse

class ApiView(View):
    """
    View sınıflarına Api desteği kazandırır.
    """
    _format = None

    def http_method_not_allowed(self, request, *args, **kwargs):
        raise ApiException('Method not allowed.', 405)

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        u"""
        Gelen istek application/x-www-form-urlencoded ile gönderilmişse
        raw_post_data içindeki veriler objeye çevrilir ve request.REQUEST güncellenir.
        """
        if django.VERSION[0] >= 1 and django.VERSION[1] > 4:
            request_body = request.body
        else:
            request_body = request.raw_post_data
        if 'application/x-www-form-urlencoded' in request.META.get('CONTENT_TYPE', '') and request.method in ['PUT']:
            request.REQUEST.dicts = (
             request.POST, request.GET, simplejson.loads(request_body))
        if 'application/json' in request.META.get('CONTENT_TYPE', ''):
            request.REQUEST.dicts = (
             request.POST, request.GET, simplejson.loads(request_body))
        try:
            try:
                if 'application/json' in request.META.get('HTTP_ACCEPT', ''):
                    self._format = 'json'
                else:
                    self._format = kwargs.get('format', 'json')
                    if self._format not in ['json', 'xml']:
                        raise ApiException('Unsupported response format.', 400)
                if kwargs.has_key('format'):
                    del kwargs['format']
                if request.REQUEST.get('method', '').lower() in self.http_method_names:
                    handler = getattr(self, request.REQUEST.get('method').lower(), self.http_method_not_allowed)
                else:
                    handler = super(ApiView, self).dispatch
                response = handler(request, *args, **kwargs)
            except ApiException as error:
                data = {'message': error.message, 
                   'status': error.status}
                if not error.application_code == None:
                    data.update({'application_code': error.application_code})
                response = ApiResponse(data, error.status)
            except Exception as error:
                response = ApiResponse({'message': 'Internal Server Error', 
                   'status': 500}, 500)

        finally:
            if isinstance(response, ApiResponse):
                status_code = response.status
                mimetype = 'text/plain'
                if self._format == 'json':
                    mimetype = 'application/json'
                elif self._format == 'xml':
                    mimetype = 'text/xml'
                response = HttpResponse(response.to_json(), '%s; charset=utf-8' % mimetype)
                response.status_code = status_code
            if request.GET.get('suppress_response_codes', False) == '1':
                response.status_code = 200
            return response