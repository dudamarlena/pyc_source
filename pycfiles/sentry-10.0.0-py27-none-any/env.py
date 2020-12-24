# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/middleware/env.py
# Compiled at: 2019-08-16 12:27:40
from __future__ import absolute_import
from django.core.signals import request_finished
from sentry.app import env

class SentryEnvMiddleware(object):

    def process_request(self, request):
        env.request = request


def clear_request(**kwargs):
    env.request = None
    return


request_finished.connect(clear_request)