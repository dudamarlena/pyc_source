# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/marcgibbons/projects/drf_signed_auth/drf_signed_auth/authentication.py
# Compiled at: 2017-09-30 09:29:48
# Size of source mod 2**32: 1144 bytes
"""
Provides Django REST Framework authentication backend
to authenticate signed URL requests.
"""
from django.core import signing
from django.utils.translation import ugettext_lazy as _
from rest_framework import authentication, exceptions
from . import settings
from .signing import UserSigner

class SignedURLAuthentication(authentication.BaseAuthentication):
    __doc__ = '\n    Authentication backend for signed URLs.\n    '

    def authenticate(self, request):
        """
        Returns authenticated user if URL signature is valid.
        """
        signer = UserSigner()
        sig = request.query_params.get(settings.SIGNED_URL_QUERY_PARAM)
        if not sig:
            return
        else:
            try:
                user = signer.unsign(sig)
            except signing.SignatureExpired:
                raise exceptions.AuthenticationFailed(_('This URL has expired.'))
            except signing.BadSignature:
                raise exceptions.AuthenticationFailed(_('Invalid signature.'))

            if not user.is_active:
                raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))
            return (
             user, None)