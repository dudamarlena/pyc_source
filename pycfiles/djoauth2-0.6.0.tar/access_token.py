# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/peterdowns/Desktop/djoauth2/djoauth2/access_token.py
# Compiled at: 2013-11-22 18:12:08
import json
from django.http import HttpResponse
from djoauth2.conf import settings
from djoauth2.errors import DJOAuthError
from djoauth2.errors import get_error_details
from djoauth2.models import AccessToken
from djoauth2.models import Scope

class AccessTokenAuthenticator(object):
    """ Allows easy authentication checking and error response creation.

  See the :py:meth:`validate` method's docstring for a usage example. We
  **strongly recommend** that you use the
  :py:func:`djoauth2.decorators.oauth_scope` decorator to protect your API
  endpoints instead of manually instatiating this object.
  """

    def __init__(self, required_scope_names=()):
        """ Store the names of the scopes that will be checked. """
        self.required_scope_names = required_scope_names

    def validate(self, request):
        """ Checks a request for proper authentication details.

    Returns a tuple of ``(access_token, error_response_arguments)``, which are
    designed to be passed to the :py:meth:`make_error_response` method.

    For example, to restrict access to a given endpoint:

    .. code-block:: python

        def foo_bar_resource(request, *args, **kwargs):
          authenticator = AccessTokenAuthenticator(
              required_scope_names=('foo', 'bar'))

          access_token, error_args = authenticator.validate(request)
          if not access_token:
            return authenticator.make_error_response(*error_args)

          # ... can now return use access_token

    :rtype: When the request validates successfully, returns a
        a tuple of (:py:class:`djoauth2.models.AccessToken`, ``None``).  If the
        request fails to validate, returns a tuple of (``None``,
        ``error_details_tuple``). The ``error_details_tuple`` is a tuple of
        arguments to use to call the :py:func:`make_error_response` method.

    """
        for name in self.required_scope_names:
            if not Scope.objects.filter(name=name).exists():
                raise ValueError(('Scope with name "{}" does not exist.').format(name))

        expose_errors = False
        try:
            if settings.DJOAUTH2_SSL_ONLY and not request.is_secure():
                raise InvalidRequest('insecure request: must use TLS')
            http_authorization = request.META.get('HTTP_AUTHORIZATION', '')
            if not http_authorization:
                raise InvalidRequest('missing HTTP_AUTHORIZATION header')
            try:
                auth_method, auth_value = http_authorization.strip().split(' ', 1)
            except ValueError:
                raise InvalidRequest('malformed HTTP_AUTHORIZATION header')

            if auth_method != 'Bearer':
                raise InvalidRequest('authentication method is not "Bearer"')
            expose_errors = True
            try:
                access_token = AccessToken.objects.get(value=auth_value)
            except AccessToken.DoesNotExist:
                raise InvalidToken('access token does not exist')

            if access_token.is_expired():
                raise InvalidToken('access token is expired')
            if not access_token.has_scope(*self.required_scope_names):
                raise InsufficientScope('access token has insufficient scope')
            return (access_token, None)
        except AuthenticationError as validation_error:
            return (
             None, (validation_error, expose_errors))

        return

    def make_error_response(self, validation_error, expose_errors):
        """ Return an appropriate ``HttpResponse`` on authentication failure.

    In case of an error, the specification only details the inclusion of the
    ``WWW-Authenticate`` header. Additionally, when allowed by the
    specification, we respond with error details formatted in JSON in the body
    of the response. For more information, read the specification:
    http://tools.ietf.org/html/rfc6750#section-3.1 .

    :param validation_error: A
      :py:class:`djoauth2.access_token.AuthenticationError` raised by the
      :py:meth:`validate` method.
    :param expose_errors: A boolean describing whether or not to expose error
      information in the error response, as described by the section of the
      specification linked to above.

    :rtype: a Django ``HttpResponse``.
    """
        authenticate_header = [
         ('Bearer realm="{}"').format(settings.DJOAUTH2_REALM)]
        if not expose_errors:
            response = HttpResponse(status=400)
            response['WWW-Authenticate'] = (', ').join(authenticate_header)
            return response
        status_code = 401
        error_details = get_error_details(validation_error)
        if isinstance(validation_error, InvalidRequest):
            status_code = 400
        else:
            if isinstance(validation_error, InvalidToken):
                status_code = 401
            elif isinstance(validation_error, InsufficientScope):
                error_details['scope'] = (' ').join(self.required_scope_names)
                status_code = 403
            response = HttpResponse(content=json.dumps(error_details), content_type='application/json', status=status_code)
            for key, value in error_details.iteritems():
                authenticate_header.append(('{}="{}"').format(key, value))

        response['WWW-Authenticate'] = (', ').join(authenticate_header)
        return response


class AuthenticationError(DJOAuthError):
    """ Base class for errors related to API request authentication.

  For more details, refer to the Bearer Token specification:

  * http://tools.ietf.org/html/rfc6750#section-3.1
  * http://tools.ietf.org/html/rfc6750#section-6.2
  """
    pass


class InvalidRequest(AuthenticationError):
    """ From http://tools.ietf.org/html/rfc6750#section-3.1 :

  The request is missing a required parameter, includes an unsupported
  parameter or parameter value, repeats the same parameter, uses more than one
  method for including an access token, or is otherwise malformed. The
  resource server SHOULD respond with the HTTP 400 (Bad Request) status code.
  """
    error_name = 'invalid_request'


class InvalidToken(AuthenticationError):
    """ From http://tools.ietf.org/html/rfc6750#section-3.1 :

  The access token provided is expired, revoked, malformed, or invalid for
  other reasons. The resource SHOULD respond with the HTTP 401 (Unauthorized)
  status code. The client MAY request a new access token and retry the
  protected resource request.
  """
    error_name = 'invalid_token'


class InsufficientScope(AuthenticationError):
    """ From http://tools.ietf.org/html/rfc6750#section-3.1 :

  The request requires higher privileges than provided by the access token.
  The resource server SHOULD respond with the HTTP 403 (Forbidden) status code
  and MAY include the "scope" attribute with the scope necessary to access the
  protected resource.
  """
    error_name = 'insufficient_scope'