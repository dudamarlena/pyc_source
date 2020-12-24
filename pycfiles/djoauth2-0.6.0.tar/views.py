# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/peterdowns/Desktop/djoauth2/djoauth2/views.py
# Compiled at: 2014-04-04 14:41:26
import json
from base64 import b64decode
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from djoauth2.conf import settings
from djoauth2.errors import DJOAuthError
from djoauth2.models import AccessToken
from djoauth2.models import AuthorizationCode
from djoauth2.models import Client
from djoauth2.models import Scope
from djoauth2.signals import refresh_token_used_after_invalidation

@csrf_exempt
def access_token_endpoint(request):
    """ Generates :py:class:`djoauth2.models.AccessTokens` if provided with
  sufficient authorization.

  This endpoint only supports two grant types:
    * ``authorization_code``: http://tools.ietf.org/html/rfc6749#section-4.1
    * ``refresh_token``: http://tools.ietf.org/html/rfc6749#section-6

  For further documentation, read http://tools.ietf.org/html/rfc6749#section-3.2
  """
    try:
        if settings.DJOAUTH2_SSL_ONLY and not request.is_secure():
            raise InvalidRequest('all token requests must use TLS')
        if not request.method == 'POST':
            raise InvalidRequest('all posts must use POST')
        client_id = None
        client_secret = None
        if 'HTTP_AUTHORIZATION' in request.META:
            try:
                http_authorization = request.META.get('HTTP_AUTHORIZATION', '')
                auth_method, auth_value = http_authorization.strip().split(' ', 1)
            except ValueError:
                raise InvalidRequest('malformed HTTP_AUTHORIZATION header')

            if not auth_method == 'Basic':
                raise InvalidRequest('unsupported HTTP_AUTHORIZATION method')
            try:
                client_id, client_secret = b64decode(auth_value).split(':')
            except (TypeError, ValueError):
                raise InvalidRequest('malformed HTTP_AUTHORIZATION value')

        if 'client_id' in request.GET or 'client_secret' in request.GET:
            raise InvalidRequest('must not include "client_id" or "client_secret" in request URI')
        if client_id and client_secret:
            if 'client_id' in request.POST or 'client_secret' in request.POST:
                raise InvalidRequest('must use only one authentication method')
        else:
            client_id = request.POST.get('client_id')
            client_secret = request.POST.get('client_secret')
        if not (client_id and client_secret):
            raise InvalidRequest('no client authentication provided')
        try:
            client = Client.objects.get(key=client_id, secret=client_secret)
        except Client.DoesNotExist:
            raise InvalidClient('client authentication failed')

        grant_type = request.POST.get('grant_type')
        if not grant_type:
            raise InvalidRequest('no "grant_type" provided')
        if grant_type == 'authorization_code':
            access_token = generate_access_token_from_authorization_code(request, client)
        elif grant_type == 'refresh_token':
            access_token = generate_access_token_from_refresh_token(request, client)
        else:
            raise UnsupportedGrantType(('"{}" is not a supported "grant_type"').format(grant_type))
        response_data = {'access_token': access_token.value, 
           'expires_in': access_token.lifetime, 
           'token_type': 'bearer', 
           'scope': (' ').join(access_token.get_scope_names_set())}
        if access_token.refreshable:
            response_data['refresh_token'] = access_token.refresh_token
        response = HttpResponse(content=json.dumps(response_data), content_type='application/json')
        response.status_code = 200
        response['Cache-Control'] = 'no-store'
        response['Pragma'] = 'no-cache'
        return response
    except AccessTokenError as generation_error:
        error_name = getattr(generation_error, 'error_name', 'invalid_request')
        error_description = str(generation_error) or 'Invalid Request.'
        response_data = {'error': error_name, 
           'error_description': error_description}
        response = HttpResponse(content=json.dumps(response_data), content_type='application/json')
        if isinstance(generation_error, InvalidClient):
            response.status_code = 401
        else:
            response.status_code = 400
        return response

    return


def generate_access_token_from_authorization_code(request, client):
    """ Generates a new AccessToken from a request with an authorization code.

  Read the specification: http://tools.ietf.org/html/rfc6749#section-4.1.3
  """
    authorization_code_value = request.POST.get('code')
    if not authorization_code_value:
        raise InvalidRequest('no "code" provided')
    try:
        authorization_code = AuthorizationCode.objects.get(value=authorization_code_value, client=client)
    except AuthorizationCode.DoesNotExist:
        raise InvalidGrant(('"{}" is not a valid "code"').format(authorization_code_value))

    if authorization_code.is_expired():
        if authorization_code.invalidated:
            for access_token in authorization_code.access_tokens.all():
                access_token.invalidate()

        raise InvalidGrant('provided "code" is expired')
    if authorization_code.redirect_uri and authorization_code.redirect_uri != request.POST.get('redirect_uri'):
        raise InvalidRequest('"redirect_uri" value must match the value from the authorization code request')
    new_access_token = AccessToken.objects.create(user=authorization_code.user, client=authorization_code.client)
    new_access_token.scopes = authorization_code.scopes.all()
    new_access_token.authorization_code = authorization_code
    new_access_token.save()
    authorization_code.invalidate()
    return new_access_token


def generate_access_token_from_refresh_token(request, client):
    """ Generates a new AccessToken from a request containing a refresh token.

  Read the specification: http://tools.ietf.org/html/rfc6749#section-6.
  """
    refresh_token_value = request.POST.get('refresh_token')
    if not refresh_token_value:
        raise InvalidRequest('no "refresh_token" provided')
    try:
        existing_access_token = AccessToken.objects.get(refresh_token=refresh_token_value, client=client)
    except AccessToken.DoesNotExist:
        raise InvalidGrant(('"{}" is not a valid "refresh_token"').format(refresh_token_value))

    if existing_access_token.invalidated:
        refresh_token_used_after_invalidation.send(sender='djoauth2', access_token=existing_access_token, request=request)
        raise InvalidGrant(('"{}" is not a valid "refresh_token"').format(refresh_token_value))
    if not existing_access_token.refreshable:
        raise InvalidGrant('access token is not refreshable')
    scope_objects = existing_access_token.scopes.all()
    new_scope_names = request.POST.get('scope', '')
    if new_scope_names:
        new_scope_names = new_scope_names.split(' ')
        if not existing_access_token.has_scope(*new_scope_names):
            raise InvalidScope('requested scopes exceed initial grant')
        scope_objects = []
        for scope_name in new_scope_names:
            try:
                scope_objects.append(Scope.objects.get(name=scope_name))
            except Scope.DoesNotExist:
                raise InvalidScope(('"{}" is not a valid scope').format(scope_name))

    requested_scope_string = request.POST.get('scope', '')
    if requested_scope_string:
        requested_scope_names = set(requested_scope_string.split(' '))
        if not requested_scope_names == existing_access_token.get_scope_names_set():
            raise InvalidScope('requested scopes do not match initial grant')
    new_access_token = AccessToken.objects.create(user=existing_access_token.user, client=existing_access_token.client)
    new_access_token.authorization_code = existing_access_token.authorization_code
    new_access_token.scopes = scope_objects
    new_access_token.save()
    existing_access_token.invalidate()
    return new_access_token


class AccessTokenError(DJOAuthError):
    """ Base class for all AccessToken-related errors.

  Read the specification: http://tools.ietf.org/html/rfc6749#section-5.2 .
  """
    pass


class InvalidRequest(AccessTokenError):
    """ From http://tools.ietf.org/html/rfc6749#section-5.2 :

  The request is missing a required parameter, includes an unsupported
  parameter value (other than grant type), repeats a parameter, includes
  multiple credentials, utilizes more than one mechanism for authenticating the
  client, or is otherwise malformed.
  """
    error_name = 'invalid_request'


class InvalidClient(AccessTokenError):
    """ From http://tools.ietf.org/html/rfc6749#section-5.2 :

  Client authentication failed (e.g., unknown client, no client authentication
  included, or unsupported authentication method). The authorization server MAY
  return an HTTP 401 (Unauthorized) status code to indicate which HTTP
  authentication schemes are supported. If the client attempted to authenticate
  via the "Authorization" request header field, the authorization server MUST
  respond with an HTTP 401 (Unauthorized) status code and include the
  "WWW-Authenticate" response header field matching the authentication scheme
  used by the client.
  """
    error_name = 'invalid_client'


class InvalidGrant(AccessTokenError):
    """ From http://tools.ietf.org/html/rfc6749#section-5.2 :

  The provided authorization grant (e.g., authorization code, resource owner
  credentials) or refresh token is invalid, expired, revoked, does not match
  the redirection URI used in the authorization request, or was issued to
  another client.
  """
    error_name = 'invalid_grant'


class UnauthorizedClient(AccessTokenError):
    """ From http://tools.ietf.org/html/rfc6749#section-5.2 :

  The authenticated client is not authorized to use this authorization grant
  type.
  """
    error_name = 'unauthorized_client'


class UnsupportedGrantType(AccessTokenError):
    """ From http://tools.ietf.org/html/rfc6749#section-5.2 :

  The authorization grant type is not supported by the authorization server.
  """
    error_name = 'unsupported_grant_type'


class InvalidScope(AccessTokenError):
    """ From http://tools.ietf.org/html/rfc6749#section-5.2 :

  The requested scope is invalid, unknown, malformed, or exceeds the scope
  granted by the resource owner.
  """
    error_name = 'invalid_scope'