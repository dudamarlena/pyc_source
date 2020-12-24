# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/th13f/dev/drf-batch-requests/drf_batch_requests/backends/sync.py
# Compiled at: 2018-02-16 09:54:40
from django.core.handlers.base import BaseHandler
from rest_framework.status import is_success
from drf_batch_requests.backends.base import RequestsConsumeBaseBackend

class SyncRequestsConsumeBackend(RequestsConsumeBaseBackend):

    def __init__(self):
        self.responses = {}

    def consume_request(self, request, start_callback=None, success_callback=None, fail_callback=None):
        start_callback() if start_callback else None
        handler = BaseHandler()
        handler.load_middleware()
        response = handler.get_response(request)
        if is_success(response.status_code):
            success_callback() if success_callback else None
        else:
            fail_callback() if fail_callback else None
        self.responses[request] = response
        return True