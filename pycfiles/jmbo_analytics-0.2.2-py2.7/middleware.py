# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo_analytics/middleware.py
# Compiled at: 2016-08-25 04:11:26
from django.conf import settings
from jmbo_analytics.utils import build_ga_params, set_cookie
from jmbo_analytics.tasks import send_ga_tracking

class GoogleAnalyticsMiddleware(object):
    """Do not use if your site is behind a reverse caching proxy"""

    def process_response(self, request, response):
        if hasattr(settings, 'GOOGLE_ANALYTICS_IGNORE_PATH'):
            exclude = [ p for p in settings.GOOGLE_ANALYTICS_IGNORE_PATH if request.path.startswith(p) ]
            if any(exclude):
                return response
        path = request.path
        referer = request.META.get('HTTP_REFERER', '')
        params = build_ga_params(request, path=path, referer=referer)
        response = set_cookie(params, response)
        send_ga_tracking.delay(params)
        return response