# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/prelaunch/middleware.py
# Compiled at: 2011-05-18 01:14:38
from django.conf import settings
from settings import *

class PrelaunchMiddleware(object):
    """ Adds a cookie to the response if a referrer parameter is present.
    """

    def process_response(self, request, response):
        """ Add or change the cookie.
        """
        prelaunch_parameter = getattr(settings, 'PRELAUNCH_PARAMETER_NAME', PRELAUNCH_PARAMETER_NAME)
        referrer = request.REQUEST.get(prelaunch_parameter, None)
        if referrer and not request.COOKIES.get('prelaunch_referrer'):
            response.set_cookie('prelaunch_referrer', referrer)
        return response