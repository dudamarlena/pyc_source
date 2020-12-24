# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/variant/middleware.py
# Compiled at: 2015-09-15 01:59:29
from __future__ import unicode_literals
from django.conf import settings
import six
from .utils import get_experiment_cookie_name

class VariantMiddleware(object):

    def process_request(self, request):
        request.variant_experiments = {}

    def process_response(self, request, response):
        experiments = getattr(request, b'variant_experiments', {})
        for name, variant in six.iteritems(experiments):
            if variant:
                cookie_name = get_experiment_cookie_name(name)
                response.set_cookie(cookie_name, variant, max_age=getattr(settings, b'VARIANT_MAX_COOKIE_AGE', 2592000), secure=getattr(settings, b'VARIANT_SECURE_COOKIE', False))

        return response