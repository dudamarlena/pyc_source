# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/paparazziaccessories-com/venv-paparazzi/src/django-browser-verification/browser_verification/middleware.py
# Compiled at: 2016-06-22 18:00:18
from .utils import verify_browser

class BrowserVerificationMiddleware(object):

    def process_request(self, request):
        verify_browser(request)