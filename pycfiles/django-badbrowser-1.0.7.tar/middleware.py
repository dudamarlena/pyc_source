# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/dev/.virtualenvs/playnicely/src/django-badbrowser/django_badbrowser/middleware.py
# Compiled at: 2012-03-16 06:35:10
import httpagentparser
from django.conf import settings
from django.core.urlresolvers import reverse
from django_badbrowser.views import unsupported
from django_badbrowser import check_user_agent

class BrowserSupportDetection(object):

    def _user_ignored_warning(self, request):
        """Has the user forced ignoring the browser warning"""
        return 'badbrowser_ignore' in request.COOKIES and request.COOKIES['badbrowser_ignore']

    def process_request(self, request):
        self._clear_cookie = False
        if request.path.startswith(settings.MEDIA_URL):
            return
        else:
            if 'HTTP_USER_AGENT' not in request.META:
                return
            else:
                user_agent = request.META['HTTP_USER_AGENT']
                parsed_user_agent = httpagentparser.detect(user_agent)
                request.browser = parsed_user_agent
                if not hasattr(settings, 'BADBROWSER_REQUIREMENTS'):
                    return
                if request.path == reverse('django-badbrowser-ignore'):
                    return
                if check_user_agent(parsed_user_agent, settings.BADBROWSER_REQUIREMENTS):
                    self._clear_cookie = True
                    return
                if self._user_ignored_warning(request):
                    return
                return unsupported(request)

            return