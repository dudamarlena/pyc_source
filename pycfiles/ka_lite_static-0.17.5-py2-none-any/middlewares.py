# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django-annoying/annoying/middlewares.py
# Compiled at: 2018-07-11 18:15:31
import re
from django.conf import settings
from django.views.static import serve
from django.shortcuts import redirect
from .exceptions import Redirect

class StaticServe(object):
    """
    Django middleware for serving static files instead of using urls.py
    """
    regex = re.compile('^%s(?P<path>.*)$' % settings.MEDIA_URL)

    def process_request(self, request):
        if settings.DEBUG:
            match = self.regex.search(request.path)
            if match:
                return serve(request, match.group(1), settings.MEDIA_ROOT)


class RedirectMiddleware(object):
    """
    You must add this middleware to MIDDLEWARE_CLASSES list,
    to make work Redirect exception. All arguments passed to
    Redirect will be passed to django built in redirect function.
    """

    def process_exception(self, request, exception):
        if not isinstance(exception, Redirect):
            return
        return redirect(*exception.args, **exception.kwargs)