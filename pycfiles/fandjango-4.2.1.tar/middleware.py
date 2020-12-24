# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jgorset/Code/python/fandjango/fandjango/middleware.py
# Compiled at: 2015-12-28 07:16:58
from django.conf import settings
from django.http import QueryDict, HttpResponseRedirect
from datetime import timedelta
from urlparse import parse_qs
from django.core.exceptions import ImproperlyConfigured
from fandjango.views import authorize_application, authorization_denied
from fandjango.models import Facebook, User, OAuthToken
from fandjango.settings import FACEBOOK_APPLICATION_SECRET_KEY, FACEBOOK_APPLICATION_ID, FANDJANGO_CACHE_SIGNED_REQUEST, DISABLED_PATHS, ENABLED_PATHS
from fandjango.utils import is_disabled_path, is_enabled_path, get_full_path, authorization_denied_view, get_post_authorization_redirect_url
from facepy import SignedRequest, GraphAPI
try:
    from django.utils.timezone import now
except ImportError:
    from datetime import datetime

    def now():
        return datetime.now()


from dateutil.tz import tzlocal

class BaseMiddleware:

    def is_valid_path(self, request):
        if ENABLED_PATHS and DISABLED_PATHS:
            raise ImproperlyConfigured('You may configure either FANDJANGO_ENABLED_PATHS or FANDJANGO_DISABLED_PATHS, but not both.')
        if DISABLED_PATHS and is_disabled_path(request.path):
            return False
        if ENABLED_PATHS and not is_enabled_path(request.path):
            return False
        return True

    def is_access_denied(self, request):
        return 'error' in request.GET and request.GET['error'] == 'access_denied'


class FacebookMiddleware(BaseMiddleware):
    """Middleware for Facebook canvas applications."""

    def process_request(self, request):
        """Process the signed request."""
        if hasattr(request, 'facebook') and request.facebook:
            return
        request.facebook = False
        if not self.is_valid_path(request):
            return
        if self.is_access_denied(request):
            return authorization_denied_view(request)
        if 'signed_request' not in request.REQUEST and 'signed_request' not in request.COOKIES:
            return
        if request.method == 'POST' and 'signed_request' in request.POST:
            request.POST = QueryDict('')
            request.method = 'GET'
        request.facebook = Facebook()
        try:
            request.facebook.signed_request = SignedRequest(signed_request=request.REQUEST.get('signed_request') or request.COOKIES.get('signed_request'), application_secret_key=FACEBOOK_APPLICATION_SECRET_KEY)
        except SignedRequest.Error:
            request.facebook = False

        if request.facebook and request.facebook.signed_request.user.has_authorized_application and not request.facebook.signed_request.user.oauth_token.has_expired:
            try:
                user = User.objects.get(facebook_id=request.facebook.signed_request.user.id)
            except User.DoesNotExist:
                oauth_token = OAuthToken.objects.create(token=request.facebook.signed_request.user.oauth_token.token, issued_at=request.facebook.signed_request.user.oauth_token.issued_at.replace(tzinfo=tzlocal()), expires_at=request.facebook.signed_request.user.oauth_token.expires_at.replace(tzinfo=tzlocal()))
                user = User.objects.create(facebook_id=request.facebook.signed_request.user.id, oauth_token=oauth_token)
                user.synchronize()
            else:
                user.last_seen_at = now()
                if 'signed_request' in request.REQUEST:
                    user.authorized = True
                    if request.facebook.signed_request.user.oauth_token:
                        user.oauth_token.token = request.facebook.signed_request.user.oauth_token.token
                        user.oauth_token.issued_at = request.facebook.signed_request.user.oauth_token.issued_at.replace(tzinfo=tzlocal())
                        user.oauth_token.expires_at = request.facebook.signed_request.user.oauth_token.expires_at.replace(tzinfo=tzlocal())
                        user.oauth_token.save()
                user.save()

            if not user.oauth_token.extended:
                try:
                    user.oauth_token.extend()
                except:
                    pass

            request.facebook.user = user

    def process_response(self, request, response):
        """
        Set compact P3P policies and save signed request to cookie.

        P3P is a WC3 standard (see http://www.w3.org/TR/P3P/), and although largely ignored by most
        browsers it is considered by IE before accepting third-party cookies (ie. cookies set by
        documents in iframes). If they are not set correctly, IE will not set these cookies.
        """
        response['P3P'] = 'CP="IDC CURa ADMa OUR IND PHY ONL COM STA"'
        if FANDJANGO_CACHE_SIGNED_REQUEST:
            if hasattr(request, 'facebook') and request.facebook and request.facebook.signed_request:
                response.set_cookie('signed_request', request.facebook.signed_request.generate())
            else:
                response.delete_cookie('signed_request')
        return response


class FacebookWebMiddleware(BaseMiddleware):
    """Middleware for Facebook auth on websites."""

    def process_request(self, request):
        """Process the web-based auth request."""
        if hasattr(request, 'facebook') and request.facebook:
            return
        else:
            request.facebook = False
            if not self.is_valid_path(request):
                return
            if self.is_access_denied(request):
                return authorization_denied_view(request)
            request.facebook = Facebook()
            oauth_token = False
            if 'oauth_token' in request.COOKIES:
                try:
                    oauth_token = OAuthToken.objects.get(token=request.COOKIES['oauth_token'])
                except OAuthToken.DoesNotExist:
                    request.facebook = False
                    return

            else:
                if 'code' in request.GET:
                    try:
                        graph = GraphAPI()
                        response = graph.get('oauth/access_token', client_id=FACEBOOK_APPLICATION_ID, redirect_uri=get_post_authorization_redirect_url(request, canvas=False), client_secret=FACEBOOK_APPLICATION_SECRET_KEY, code=request.GET['code'])
                        components = parse_qs(response)
                        oauth_token, new_oauth_token = OAuthToken.objects.get_or_create(token=components['access_token'][0], issued_at=now(), expires_at=now() + timedelta(seconds=int(components['expires'][0])))
                    except GraphAPI.OAuthError:
                        pass

                if not oauth_token or oauth_token.expired:
                    request.facebook = False
                    return
                try:
                    user = oauth_token.user
                    if not user.authorized:
                        request.facebook = False
                        return
                    user.last_seen_at = now()
                    user.save()
                except User.DoesNotExist:
                    graph = GraphAPI(oauth_token.token)
                    profile = graph.get('me')
                    try:
                        user = User.objects.get(facebook_id=profile.get('id'))
                        if not user.authorized:
                            if new_oauth_token:
                                user.last_seen_at = now()
                                user.authorized = True
                            else:
                                request.facebook = False
                                return
                    except User.DoesNotExist:
                        user = User.objects.create(facebook_id=profile.get('id'), oauth_token=oauth_token)

                    user.synchronize(profile)
                    old_oauth_token = None
                    if user.oauth_token != oauth_token:
                        old_oauth_token = user.oauth_token
                        user.oauth_token = oauth_token
                    user.save()
                    if old_oauth_token:
                        old_oauth_token.delete()

            if not user.oauth_token.extended:
                try:
                    user.oauth_token.extend()
                except:
                    pass

            request.facebook.user = user
            request.facebook.oauth_token = oauth_token
            return

    def process_response(self, request, response):
        """
        Set compact P3P policies and save auth token to cookie.

        P3P is a WC3 standard (see http://www.w3.org/TR/P3P/), and although largely ignored by most
        browsers it is considered by IE before accepting third-party cookies (ie. cookies set by
        documents in iframes). If they are not set correctly, IE will not set these cookies.
        """
        if hasattr(request, 'facebook') and request.facebook and request.facebook.oauth_token:
            if 'code' in request.REQUEST:
                path = get_full_path(request, remove_querystrings=['code', 'web_canvas'])
                response = HttpResponseRedirect(path)
            response.set_cookie('oauth_token', request.facebook.oauth_token.token)
        else:
            response.delete_cookie('oauth_token')
        response['P3P'] = 'CP="IDC CURa ADMa OUR IND PHY ONL COM STA"'
        return response