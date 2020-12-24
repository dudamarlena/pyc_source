# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/auth_index.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from django.contrib.auth import logout
from django.contrib.auth.models import AnonymousUser
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from sentry.api.authentication import QuietBasicAuthentication
from sentry.api.base import Endpoint
from sentry.api.serializers import DetailedUserSerializer, serialize
from sentry.api.validators import AuthVerifyValidator
from sentry.models import Authenticator
from sentry.utils import auth, json
from sentry.utils.functional import extract_lazy_object

class AuthIndexEndpoint(Endpoint):
    """
    Manage session authentication

    Intended to be used by the internal Sentry application to handle
    authentication methods from JS endpoints by relying on internal sessions
    and simple HTTP authentication.
    """
    authentication_classes = [
     QuietBasicAuthentication, SessionAuthentication]
    permission_classes = ()

    def get(self, request):
        if not request.user.is_authenticated():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        user = extract_lazy_object(request._request.user)
        return Response(serialize(user, user, DetailedUserSerializer()))

    def post(self, request):
        """
        Authenticate a User
        ```````````````````

        This endpoint authenticates a user using the provided credentials
        through a regular HTTP basic auth system.  The response contains
        cookies that need to be sent with further requests that require
        authentication.

        This is primarily used internally in Sentry.

        Common example::

            curl -X ###METHOD### -u username:password ###URL###
        """
        if not request.user.is_authenticated():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        if Authenticator.objects.user_has_2fa(request.user):
            return Response({'2fa_required': True, 
               'message': 'Cannot sign-in with password authentication when 2fa is enabled.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            auth.login(request._request, request.user)
        except auth.AuthUserPasswordExpired:
            return Response({'message': 'Cannot sign-in with password authentication because password has expired.'}, status=status.HTTP_403_FORBIDDEN)

        request.user = request._request.user
        return self.get(request)

    def put(self, request):
        """
        Verify a User
        `````````````

        This endpoint verifies the currently authenticated user (for example, to gain superuser).

        :auth: required
        """
        if not request.user.is_authenticated():
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        validator = AuthVerifyValidator(data=request.data)
        if not validator.is_valid():
            return self.respond(validator.errors, status=status.HTTP_400_BAD_REQUEST)
        authenticated = False
        if 'challenge' in validator.validated_data and 'response' in validator.validated_data:
            try:
                interface = Authenticator.objects.get_interface(request.user, 'u2f')
                if not interface.is_enrolled:
                    raise LookupError()
                challenge = json.loads(validator.validated_data['challenge'])
                response = json.loads(validator.validated_data['response'])
                authenticated = interface.validate_response(request, challenge, response)
            except ValueError:
                pass
            except LookupError:
                pass

        else:
            authenticated = request.user.check_password(validator.validated_data['password'])
        if not authenticated:
            return Response({'detail': {'code': 'ignore'}}, status=status.HTTP_403_FORBIDDEN)
        try:
            auth.login(request._request, request.user)
        except auth.AuthUserPasswordExpired:
            return Response({'code': 'password-expired', 
               'message': 'Cannot sign-in with basic auth because password has expired.'}, status=status.HTTP_403_FORBIDDEN)

        request.user = request._request.user
        return self.get(request)

    def delete(self, request, *args, **kwargs):
        """
        Logout the Authenticated User
        `````````````````````````````

        Deauthenticate the currently active session. Can also deactivate
        all sessions for a user if the ``all`` parameter is sent.
        """
        if request.data.get('all'):
            request.user.refresh_session_nonce()
            request.user.save()
        logout(request._request)
        request.user = AnonymousUser()
        return Response(status=status.HTTP_204_NO_CONTENT)