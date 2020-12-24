# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/yuji/Projects/Grove/grove_project/grove/../grove/website/redirects/middleware.py
# Compiled at: 2012-05-30 17:48:10
"""
Redirect Middleware
-------------------

Get cached copy of redirects and apply if match found
# must be in memory - don't execute a DB call every time a page is hit

Created on Wednesday, May 2012 by Yuji Tomita
"""
import logging
from django import http
from django.core.cache import cache
from grove.website.redirects.models import Redirect
log = logging.getLogger(__name__)

class RedirectMiddleware(object):

    def process_request(self, request):
        try:
            redirect_url = Redirect.objects.get_redirect_for_path(request.path)
            if redirect_url:
                return http.HttpResponsePermanentRedirect(redirect_url)
        except Exception as e:
            log.critical(('Exception fired on Redirect Middleware catch all! {0}').format(e))

        return