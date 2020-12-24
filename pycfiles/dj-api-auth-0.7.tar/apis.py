# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/fanfei/Documents/Code/dj-api-auth/example/djapp/djapp/apis.py
# Compiled at: 2015-06-06 19:40:47
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from djapiauth import api_auth
from djapiauth import AuthMixin

@csrf_exempt
@api_auth
def apicall(request):
    if request.method == 'GET':
        return HttpResponse(json.dumps({'message': 'goodbye', 'method': 'get'}))
    else:
        return HttpResponse(json.dumps({'message': 'goodbye,' + request.body, 'method': 'post'}))


class ProtectedView(AuthMixin, View):

    def get(self, request):
        return HttpResponse(json.dumps({'message': 'hello, auth from get'}))

    def post(self, request):
        return HttpResponse(json.dumps({'message': 'hello, auth from post', 'body': request.body}))


class UnprotectedView(AuthMixin, View):
    api_auth = False

    def get(self, request):
        return HttpResponse(json.dumps({'message': 'no auth needed'}))