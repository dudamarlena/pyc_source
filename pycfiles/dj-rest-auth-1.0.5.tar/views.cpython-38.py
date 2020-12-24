# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/michael/Projects/dj-rest-auth/dj_rest_auth/views.py
# Compiled at: 2020-04-16 02:58:10
# Size of source mod 2**32: 10282 bytes
from django.conf import settings
from django.contrib.auth import get_user_model
import django.contrib.auth as django_login
import django.contrib.auth as django_logout
from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
import django.utils.translation as _
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .app_settings import JWTSerializer, LoginSerializer, PasswordChangeSerializer, PasswordResetConfirmSerializer, PasswordResetSerializer, TokenSerializer, UserDetailsSerializer, create_token
from .models import TokenModel
from .utils import jwt_encode
sensitive_post_parameters_m = method_decorator(sensitive_post_parameters('password', 'old_password', 'new_password1', 'new_password2'))

class LoginView(GenericAPIView):
    __doc__ = "\n    Check the credentials and return the REST Token\n    if the credentials are valid and authenticated.\n    Calls Django Auth login method to register User ID\n    in Django session framework\n\n    Accept the following POST parameters: username, password\n    Return the REST Framework Token Object's key.\n    "
    permission_classes = (
     AllowAny,)
    serializer_class = LoginSerializer
    token_model = TokenModel

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return (super(LoginView, self).dispatch)(*args, **kwargs)

    def process_login(self):
        django_login(self.request, self.user)

    def get_response_serializer(self):
        if getattr(settings, 'REST_USE_JWT', False):
            response_serializer = JWTSerializer
        else:
            response_serializer = TokenSerializer
        return response_serializer

    def login(self):
        self.user = self.serializer.validated_data['user']
        if getattr(settings, 'REST_USE_JWT', False):
            self.access_token, self.refresh_token = jwt_encode(self.user)
        else:
            self.token = create_token(self.token_model, self.user, self.serializer)
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            self.process_login()

    def get_response(self):
        serializer_class = self.get_response_serializer()
        if getattr(settings, 'REST_USE_JWT', False):
            data = {'user':self.user,  'access_token':self.access_token, 
             'refresh_token':self.refresh_token}
            serializer = serializer_class(instance=data, context={'request': self.request})
        else:
            serializer = serializer_class(instance=(self.token), context={'request': self.request})
        response = Response((serializer.data), status=(status.HTTP_200_OK))
        if getattr(settings, 'REST_USE_JWT', False):
            cookie_name = getattr(settings, 'JWT_AUTH_COOKIE', None)
            import rest_framework_simplejwt.settings as jwt_settings
            if cookie_name:
                from datetime import datetime
                expiration = datetime.utcnow() + jwt_settings.ACCESS_TOKEN_LIFETIME
                response.set_cookie(cookie_name,
                  (self.access_token),
                  expires=expiration,
                  httponly=True)
        return response

    def post(self, request, *args, **kwargs):
        self.request = request
        self.serializer = self.get_serializer(data=(self.request.data), context={'request': request})
        self.serializer.is_valid(raise_exception=True)
        self.login()
        return self.get_response()


class LogoutView(APIView):
    __doc__ = '\n    Calls Django logout method and delete the Token object\n    assigned to the current User object.\n\n    Accepts/Returns nothing.\n    '
    permission_classes = (
     AllowAny,)

    def get(self, request, *args, **kwargs):
        if getattr(settings, 'ACCOUNT_LOGOUT_ON_GET', False):
            response = self.logout(request)
        else:
            response = (self.http_method_not_allowed)(request, *args, **kwargs)
        return (self.finalize_response)(request, response, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.logout(request)

    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        else:
            if getattr(settings, 'REST_SESSION_LOGIN', True):
                django_logout(request)
            else:
                response = Response({'detail': _('Successfully logged out.')}, status=(status.HTTP_200_OK))
                if getattr(settings, 'REST_USE_JWT', False):
                    from rest_framework_simplejwt.exceptions import TokenError
                    from rest_framework_simplejwt.tokens import RefreshToken
                    cookie_name = getattr(settings, 'JWT_AUTH_COOKIE', None)
                    if cookie_name:
                        response.delete_cookie(cookie_name)
                    else:
                        if 'rest_framework_simplejwt.token_blacklist' in settings.INSTALLED_APPS:
                            try:
                                token = RefreshToken(request.data['refresh'])
                                token.blacklist()
                            except KeyError:
                                response = Response({'detail': _('Refresh token was not included in request data.')}, status=(status.HTTP_401_UNAUTHORIZED))
                            except (TokenError, AttributeError, TypeError) as error:
                                try:
                                    if hasattr(error, 'args'):
                                        if 'Token is blacklisted' in error.args or 'Token is invalid or expired' in error.args:
                                            response = Response({'detail': _(error.args[0])}, status=(status.HTTP_401_UNAUTHORIZED))
                                        else:
                                            response = Response({'detail': _('An error has occurred.')}, status=(status.HTTP_500_INTERNAL_SERVER_ERROR))
                                    else:
                                        response = Response({'detail': _('An error has occurred.')}, status=(status.HTTP_500_INTERNAL_SERVER_ERROR))
                                finally:
                                    error = None
                                    del error

                        else:
                            response = Response({'detail': _('Neither cookies or blacklist are enabled, so the token has not been deleted server side. Please make sure the token is deleted client side.')},
                              status=(status.HTTP_200_OK))
            return response


class UserDetailsView(RetrieveUpdateAPIView):
    __doc__ = '\n    Reads and updates UserModel fields\n    Accepts GET, PUT, PATCH methods.\n\n    Default accepted fields: username, first_name, last_name\n    Default display fields: pk, username, email, first_name, last_name\n    Read-only fields: pk, email\n\n    Returns UserModel fields.\n    '
    serializer_class = UserDetailsSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user

    def get_queryset(self):
        """
        Adding this method since it is sometimes called when using
        django-rest-swagger
        """
        return get_user_model().objects.none()


class PasswordResetView(GenericAPIView):
    __doc__ = '\n    Calls Django Auth PasswordResetForm save method.\n\n    Accepts the following POST parameters: email\n    Returns the success/fail message.\n    '
    serializer_class = PasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=(request.data))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': _('Password reset e-mail has been sent.')},
          status=(status.HTTP_200_OK))


class PasswordResetConfirmView(GenericAPIView):
    __doc__ = "\n    Password reset e-mail link is confirmed, therefore\n    this resets the user's password.\n\n    Accepts the following POST parameters: token, uid,\n        new_password1, new_password2\n    Returns the success/fail message.\n    "
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return (super(PasswordResetConfirmView, self).dispatch)(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=(request.data))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': _('Password has been reset with the new password.')})


class PasswordChangeView(GenericAPIView):
    __doc__ = '\n    Calls Django Auth SetPasswordForm save method.\n\n    Accepts the following POST parameters: new_password1, new_password2\n    Returns the success/fail message.\n    '
    serializer_class = PasswordChangeSerializer
    permission_classes = (IsAuthenticated,)

    @sensitive_post_parameters_m
    def dispatch(self, *args, **kwargs):
        return (super(PasswordChangeView, self).dispatch)(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=(request.data))
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'detail': _('New password has been saved.')})