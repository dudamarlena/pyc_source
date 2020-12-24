# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lxsameer/src/daarmaan/gauth/middlewares.py
# Compiled at: 2012-06-27 12:44:11
import time
from django.conf import settings
from django.utils.cache import patch_vary_headers
from django.utils.http import cookie_date
from django.utils.importlib import import_module

class SessionMiddleware(object):

    def process_request(self, request):
        engine = import_module(settings.SESSION_ENGINE)
        print 'TEST: cookies: ', request.COOKIES
        session_key = request.COOKIES.get(settings.SESSION_COOKIE_NAME, None)
        print 'TEST: key: ', session_key
        request.session = engine.SessionStore(session_key)
        return

    def process_response(self, request, response):
        """
        If request.session was modified, or if the configuration is to save the
        session every time, save the changes and set a session cookie.
        """
        try:
            accessed = request.session.accessed
            modified = request.session.modified
        except AttributeError:
            pass

        if accessed:
            patch_vary_headers(response, ('Cookie', ))
        if modified or settings.SESSION_SAVE_EVERY_REQUEST:
            if request.session.get_expire_at_browser_close():
                max_age = None
                expires = None
            else:
                max_age = request.session.get_expiry_age()
                expires_time = time.time() + max_age
                expires = cookie_date(expires_time)
            request.session.save()
            response.set_cookie(settings.SESSION_COOKIE_NAME, request.session.session_key, max_age=max_age, expires=expires, domain=settings.SESSION_COOKIE_DOMAIN, path=settings.SESSION_COOKIE_PATH, secure=settings.SESSION_COOKIE_SECURE or None, httponly=settings.SESSION_COOKIE_HTTPONLY or None)
        return response