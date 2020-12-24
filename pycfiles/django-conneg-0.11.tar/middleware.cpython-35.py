# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kebl2765/Projects/django-conneg/django_conneg/support/middleware.py
# Compiled at: 2014-10-28 11:46:48
# Size of source mod 2**32: 5291 bytes
import base64
try:
    from http.client import UNAUTHORIZED, FORBIDDEN, FOUND
    import urllib.parse as urllib_parse
except ImportError:
    from httplib import UNAUTHORIZED, FORBIDDEN, FOUND
    import urlparse as urllib_parse

from django.conf import settings
from django.contrib.auth import authenticate
from django_conneg.http import MediaType
from django_conneg.views import HTMLView, JSONPView, TextView

class UnauthorizedView(HTMLView, JSONPView, TextView):
    _force_fallback_format = 'txt'
    template_name = 'conneg/unauthorized'

    def get(self, request):
        self.context.update({'status_code': UNAUTHORIZED, 
         'error': 'You need to be authenticated to perform this request.'})
        return self.render()

    post = put = delete = get


class InactiveUserView(HTMLView, JSONPView, TextView):
    _force_fallback_format = 'txt'
    template_name = 'conneg/inactive_user'

    def get(self, request):
        self.context.update({'status_code': FORBIDDEN, 
         'error': 'Your account is inactive.'})
        return self.render()

    post = put = delete = get


class BasicAuthMiddleware(object):
    __doc__ = '\n    Sets request.user if there are valid basic auth credentials on the\n    request, and turns @login_required redirects into 401 responses for\n    non-HTML responses.\n    '
    allow_http = getattr(settings, 'BASIC_AUTH_ALLOW_HTTP', False) or settings.DEBUG
    unauthorized_view = staticmethod(UnauthorizedView.as_view())
    inactive_user_view = staticmethod(InactiveUserView.as_view())

    def process_request(self, request):
        if request.user.is_authenticated():
            return
        if not self.allow_http and not request.is_secure():
            return
        authorization = request.META.get('HTTP_AUTHORIZATION')
        if not authorization or not authorization.startswith('Basic '):
            return
            try:
                credentials = base64.b64decode(authorization[6:].encode('utf-8')).decode('utf-8').split(':', 1)
            except TypeError:
                return

            if len(credentials) != 2:
                return
            user = authenticate(username=credentials[0], password=credentials[1])
            if user and user.is_active:
                request.user = user
        else:
            if user and not user.is_active:
                return self.inactive_user_view(request)
            else:
                return self.unauthorized_view(request)

    def process_response(self, request, response):
        """
        Adds WWW-Authenticate: Basic headers to 401 responses, and rewrites
        redirects the login page to be 401 responses if it's a non-browser
        agent.
        """
        process = False
        if not self.allow_http and not request.is_secure():
            return response
        if response.status_code == UNAUTHORIZED:
            pass
        else:
            if response.status_code == FOUND:
                location = urllib_parse.urlparse(response['Location'])
                if location.path != settings.LOGIN_URL:
                    return response
                return self.is_agent_a_robot(request) or response
            realm = getattr(settings, 'BASIC_AUTH_REALM', request.META.get('HTTP_HOST', 'restricted'))
            if response.status_code == FOUND:
                response = self.unauthorized_view(request)
            authenticate = response.get('WWW-Authenticate', None)
            if authenticate:
                authenticate = 'Basic realm="%s", %s' % (realm, authenticate)
            else:
                authenticate = 'Basic realm="%s"' % realm
            response['WWW-Authenticate'] = authenticate
        return response

    def is_agent_a_robot(self, request):
        if request.META.get('HTTP_ORIGIN'):
            return True
        if request.META.get('HTTP_X_REQUESTED_WITH'):
            return True
        accept = sorted(MediaType.parse_accept_header(request.META.get('HTTP_ACCEPT', '')), reverse=True)
        if accept and accept[0].type in (('text', 'html', None), ('application', 'xml', 'xhtml')):
            return False
        if 'MSIE' in request.META.get('HTTP_USER_AGENT', ''):
            return False
        return True