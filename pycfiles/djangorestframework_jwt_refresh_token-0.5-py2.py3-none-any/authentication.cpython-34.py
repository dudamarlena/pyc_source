# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/src/django-rest-framework-jwt/rest_framework_jwt/refreshtoken/authentication.py
# Compiled at: 2015-11-14 11:42:20
# Size of source mod 2**32: 1548 bytes
from django.utils.translation import ugettext as _
from rest_framework.authentication import TokenAuthentication, get_authorization_header
from rest_framework import exceptions
from rest_framework_jwt.refreshtoken.models import RefreshToken

class RefreshTokenAuthentication(TokenAuthentication):
    __doc__ = '\n    Subclassed from rest_framework.authentication.TokenAuthentication\n\n    Auth header:\n        Authorization: RefreshToken 401f7ac837da42b97f613d789819ff93537bee6a\n    '
    model = RefreshToken

    def authenticate(self, request):
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != b'refreshtoken':
            return
        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)
        return self.authenticate_credentials(auth[1])

    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.select_related('user').get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))
        return (token.user, token)

    def authenticate_header(self, request):
        return 'RefreshToken'