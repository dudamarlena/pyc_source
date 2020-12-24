# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/middleware/health.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import itertools, six
from django.http import HttpResponse

class HealthCheck(object):

    def process_request(self, request):
        if request.path != '/_health/':
            return
        if 'full' not in request.GET:
            return HttpResponse('ok', content_type='text/plain')
        from sentry.status_checks import Problem, check_all
        from sentry.utils import json
        threshold = Problem.threshold(Problem.SEVERITY_CRITICAL)
        results = {check:filter(threshold, problems) for check, problems in check_all().items()}
        problems = list(itertools.chain.from_iterable(results.values()))
        return HttpResponse(json.dumps({'problems': [ six.text_type(p) for p in problems ], 'healthy': {type(check).__name__:not p for check, p in results.items()}}), content_type='application/json', status=500 if problems else 200)