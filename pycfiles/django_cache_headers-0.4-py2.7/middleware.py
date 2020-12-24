# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cache_headers/middleware.py
# Compiled at: 2018-07-07 04:58:09
import hashlib, logging, re, uuid
from importlib import import_module
from django.conf import settings
from django.contrib.auth import SESSION_KEY
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.core.cache import cache
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.utils.deprecation import MiddlewareMixin
from cache_headers import policies
POLICIES = {'all-users': policies.all_users, 
   'anonymous-only': policies.anonymous_only, 
   'anonymous-and-authenticated': policies.anonymous_and_authenticated, 
   'per-user': policies.per_user}
try:
    POLICIES.update(settings.CACHE_HEADERS['policies'])
except (KeyError, AttributeError):
    pass

try:
    TIMEOUTS = settings.CACHE_HEADERS['timeouts']
except (KeyError, AttributeError):
    TIMEOUTS = {}

rules = []
for cache_type in TIMEOUTS.keys():
    for timeout, strings in TIMEOUTS[cache_type].items():
        for s in strings:
            rules.append((re.compile('' + s), timeout, cache_type, len(s)))

rules.sort(key=lambda x: x[3], reverse=True)

def on_user_auth_event(sender, user, request, **kwargs):
    setattr(request, '_dch_auth_event', True)


user_logged_in.connect(on_user_auth_event)
user_logged_out.connect(on_user_auth_event)

class CacheHeadersMiddleware(MiddlewareMixin):
    """Put this middleware before authentication middleware because response
    runs in reverse order."""

    def process_response(self, request, response):
        if settings.DEBUG:
            return response
        else:
            user = getattr(request, 'user', None)
            if not user:
                return response
            if hasattr(request, '_dch_auth_event'):
                if user.is_authenticated:
                    if request.session.get_expire_at_browser_close():
                        response.set_cookie('isauthenticated', 1, max_age=None)
                    else:
                        expires = request.session.get_expiry_date()
                        response.set_cookie('isauthenticated', 1, expires=expires)
                else:
                    response.delete_cookie('isauthenticated')
            if 'Cache-Control' in response or 'cache-control' in response:
                return response
            if response.status_code != 200:
                return response
            response['Cache-Control'] = 'no-cache'
            if hasattr(request, '_dch_auth_event'):
                return response
            if settings.SESSION_COOKIE_NAME in request.COOKIES:
                cookie = request.COOKIES[settings.SESSION_COOKIE_NAME]
                sessionid = getattr(cookie, 'value', cookie)
                if sessionid:
                    store = import_module(settings.SESSION_ENGINE).SessionStore(SESSION_KEY)
                    if not store._validate_session_key(sessionid):
                        return HttpResponseBadRequest('User has an invalid sessionid')
            if getattr(settings, 'CACHE_HEADERS', {}).get('enable-tampering-checks', False):
                if user.is_anonymous:
                    value = request.COOKIES.get('isauthenticated', None)
                    if value not in (None, ''):
                        return HttpResponseBadRequest('User is anonymous but sent an isauthenticated cookie')
                if user.is_authenticated:
                    value = request.COOKIES.get('isauthenticated', None)
                    if value != '1':
                        return HttpResponseBadRequest('User is authenticated, but did not send valid isauthenticated cookie')
            if request.method.lower() not in ('get', 'head'):
                return response
            if response.has_header('Set-Cookie'):
                logger = logging.getLogger('django')
                logger.warn('Attempting to cache path %s but Set-Cookie is on the response' % request.get_full_path())
                return response
            full_path = request.get_full_path()
            key = 'dch-%s' % hashlib.md5(full_path.encode('utf-8')).hexdigest()
            cached = cache.get(key, None)
            if cached is not None:
                age = cached['age']
                cache_type = cached['cache_type']
            else:
                age = 0
                cache_type = None
                for pattern, timeout, cache_type, _ in rules:
                    if pattern.match(full_path):
                        age = timeout
                        break

                cache.set(key, {'age': age, 'cache_type': cache_type}, 86400)
            if age and request:
                pth = full_path
                if 'dch-uuid=' in pth:
                    return response
                l = 0
                try:
                    l = len(request._messages)
                except (AttributeError, TypeError):
                    pass

                if l:
                    if '?' in pth:
                        pth += '&dch-uuid='
                    else:
                        pth += '?dch-uuid='
                    pth += str(uuid.uuid1())
                    return HttpResponseRedirect(pth)
            if age:
                policy = POLICIES[cache_type]
                policy(request, response, user, age)
            else:
                response['Cache-Control'] = 'no-cache'
            return response