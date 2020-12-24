# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/sites/middleware.py
# Compiled at: 2019-02-14 00:35:17
from django.utils.deprecation import MiddlewareMixin
from .shortcuts import get_current_site

class CurrentSiteMiddleware(MiddlewareMixin):
    """
    Middleware that sets `site` attribute to request object.
    """

    def process_request(self, request):
        request.site = get_current_site(request)