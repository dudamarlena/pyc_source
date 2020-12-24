# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/michael/Projects/dj-rest-auth/dj_rest_auth/app_settings.py
# Compiled at: 2020-04-18 13:56:51
# Size of source mod 2**32: 1761 bytes
import dj_rest_auth.serializers as DefaultJWTSerializer
import dj_rest_auth.serializers as DefaultLoginSerializer
import dj_rest_auth.serializers as DefaultPasswordChangeSerializer
import dj_rest_auth.serializers as DefaultPasswordResetConfirmSerializer
import dj_rest_auth.serializers as DefaultPasswordResetSerializer
import dj_rest_auth.serializers as DefaultTokenSerializer
import dj_rest_auth.serializers as DefaultUserDetailsSerializer
from django.conf import settings
from .utils import default_create_token, import_callable
create_token = import_callable(getattr(settings, 'REST_AUTH_TOKEN_CREATOR', default_create_token))
serializers = getattr(settings, 'REST_AUTH_SERIALIZERS', {})
TokenSerializer = import_callable(serializers.get('TOKEN_SERIALIZER', DefaultTokenSerializer))
JWTSerializer = import_callable(serializers.get('JWT_SERIALIZER', DefaultJWTSerializer))
UserDetailsSerializer = import_callable(serializers.get('USER_DETAILS_SERIALIZER', DefaultUserDetailsSerializer))
LoginSerializer = import_callable(serializers.get('LOGIN_SERIALIZER', DefaultLoginSerializer))
PasswordResetSerializer = import_callable(serializers.get('PASSWORD_RESET_SERIALIZER', DefaultPasswordResetSerializer))
PasswordResetConfirmSerializer = import_callable(serializers.get('PASSWORD_RESET_CONFIRM_SERIALIZER', DefaultPasswordResetConfirmSerializer))
PasswordChangeSerializer = import_callable(serializers.get('PASSWORD_CHANGE_SERIALIZER', DefaultPasswordChangeSerializer))
JWT_AUTH_COOKIE = getattr(settings, 'JWT_AUTH_COOKIE', None)