# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/th13f/dev/drf-batch-requests/drf_batch_requests/backends/base.py
# Compiled at: 2018-02-16 08:43:58


class RequestsConsumeBaseBackend(object):

    def consume_request(self, request, start_callback=None, success_callback=None, fail_callback=None):
        raise NotImplementedError