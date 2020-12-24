# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/th13f/dev/drf-batch-requests/drf_batch/views.py
# Compiled at: 2017-10-11 09:00:50
# Size of source mod 2**32: 1600 bytes
import json
from django.core.handlers.base import BaseHandler
from rest_framework.response import Response
from rest_framework.status import is_success
from rest_framework.views import APIView
from .request import BatchRequestsFactory

class BatchView(APIView):

    def post(self, request, *args, **kwargs):
        responses = []
        requests_factory = BatchRequestsFactory(request)
        for current_request in requests_factory:
            handler = BaseHandler()
            handler.load_middleware()
            response = handler.get_response(current_request)
            result = {'code': response.status_code, 
             'headers': [{'name': key, 'value': value} for key, value in response._headers.values()], 
             
             'body': response.content.decode('utf-8')}
            if is_success(response.status_code):
                result['_data'] = json.loads(result['body'])
            if not is_success(response.status_code) or is_success(response.status_code) and not current_request.omit_response_on_success:
                result['return_body'] = True
            if current_request.name:
                requests_factory.named_responses[current_request.name] = result
            responses.append({k:v for k, v in result.items() if not k.startswith('_') if not k.startswith('_')})
            if not is_success(response.status_code):
                break

        return self.finalize_response(request, Response(responses))