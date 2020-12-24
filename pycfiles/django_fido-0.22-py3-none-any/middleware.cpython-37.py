# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jmusilek/github/django-fido/django_fido/middleware.py
# Compiled at: 2020-02-18 05:19:49
# Size of source mod 2**32: 1287 bytes
"""django-fido middlewares."""
from __future__ import unicode_literals
from django.http import HttpResponseRedirect
from .settings import SETTINGS

class Fido2AuthenticationMiddleware:
    __doc__ = '\n    Middleware that ensures additional FIDO2 authentication.\n\n    Additional FIDO2 authentication is required for all users if DJANGO_FIDO_FORCE_2FA is True.\n    Otherwise, additional FIDO2 authentication is required only if user has any associated authenticator.\n    User without additional FIDO2 authentication is redirected on additional authentication page.\n    '
    FIDO2_AUTHENTICATION_BACKEND = 'django_fido.backends.Fido2AuthenticationBackend'

    def __init__(self, get_response):
        """Initialize middleware."""
        self.get_response = get_response

    def __call__(self, request):
        """Redirect user without FIDO2 authentication."""
        if request.user.is_authenticated:
            if request.get_full_path() != SETTINGS.redirect_2fa:
                auth_backend = request.session.get('_auth_user_backend')
                if auth_backend != self.FIDO2_AUTHENTICATION_BACKEND:
                    if SETTINGS.force_2fa or request.user.authenticators.count() > 0:
                        return HttpResponseRedirect(SETTINGS.redirect_2fa)
        return self.get_response(request)