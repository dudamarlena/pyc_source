# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/peterdowns/Desktop/djoauth2/djoauth2/authorization.py
# Compiled at: 2013-11-22 18:12:08
from urllib import urlencode
from urlparse import urlparse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
try:
    from django.http.request import absolute_http_url_re
except ImportError:
    from django.http import absolute_http_url_re

from django.shortcuts import render
from django.forms import Form
from django.views.decorators.http import require_http_methods
from djoauth2.conf import settings
from djoauth2.errors import DJOAuthError
from djoauth2.errors import get_error_details
from djoauth2.helpers import update_parameters
from djoauth2.models import AuthorizationCode
from djoauth2.models import Client
from djoauth2.models import Scope

class AuthorizationCodeGenerator(object):
    """ Allows easy authorization request validation, code generation, and
  redirection creation.

  Use as part of your authorization page endpoint like so:

  .. code-block:: python

      def authorization(request):
        auth_code_generator = AuthorizationCodeGenerator(
            '/oauth2/missing_redirect_uri/')
        try:
          auth_code_generator.validate(request)
        except AuthorizationError as e:
          return auth_code_generator.make_error_redirect()

        if request.method == 'GET':
          # Show a page for the user to see the scope request. Include a form
          # for the user to authorize or reject the request. Make sure to
          # include all of the # original authorization request's parameters
          # with the form so that they # can be accessed when the user submits
          # the form.
          original_request_parameters = (
              auth_code_generator.get_request_uri_parameters())
          # See the template example below.
          template_render_context = {
              'form': Form(),
              'client': auth_code_generator.client,
              'scopes': auth_code_generator.valid_scope_objects,
              # Assumes that this endpoint is connected to
              # the '/oauth/authorization/' URL.
              'form_action': ('/oauth2/authorization/?' +
                              original_request_parameters),
            }
          return render(request,
                        'oauth2server/authorization_page.html',
                        template_render_context)
        elif request.method == 'POST':
          # Check the form the user submits (see the template below.)
          if request.POST.get('user_action') == 'Accept':
            return auth_code_generator.make_success_redirect()
          else:
            return auth_code_generator.make_error_redirect()

  An example template (``'oauth2server/authorization_page.html'`` from the
  above example) should look something like this:

  .. code-block:: html+django

      <p>{{client.name}} is requesting access to the following scopes:</p>

      <ul>
        {% for scope in scopes %}
        <li> <b>{{scope.name}}</b>: {{scope.description}} </li>
        {% endfor %}
      </ul>

      <form action="{{form_action}}" method="POST">
        {% csrf_token %}
        <div style="display: none;"> {{form}} </div>
        <input type="submit" name="user_action" value="Decline"/>
        <input type="submit" name="user_action" value="Accept"/>
      </form>

  We **strongly recommend** that you avoid instantiating this class. Instead,
  prefer the :py:func:`djoauth2.authorization.make_authorization_endpoint`
  """

    def __init__(self, missing_redirect_uri):
        """ Create a new AuthorizationCodeGenerator.

    :param missing_redirect_uri: a string URI to which to redirect the user if
        the authorization request is not valid and no redirect is able to be
        parsed from the request.
    """
        self.missing_redirect_uri = missing_redirect_uri
        self.user = None
        self.client = None
        self.redirect_uri = None
        self.request_redirect_uri = None
        self.valid_scope_objects = None
        self.state = None
        self.request = None
        return

    def validate(self, request):
        """ Check that a Client's authorization request is valid.

    If the request is invalid or malformed in any way, raises the appropriate
    exception.  Read `the relevant section of the specification
    <http://tools.ietf.org/html/rfc6749#section-4.1 .>`_ for descriptions of
    each type of error.

    :raises: a :py:class:`AuthorizationError` if the request is invalid.
    """
        if request.method not in ('GET', 'POST'):
            raise InvalidRequest('must be GET or POST request')
        if settings.DJOAUTH2_SSL_ONLY and not request.is_secure():
            raise InvalidRequest('all requests must use TLS')
        self.request = request
        self.user = request.user
        if not self.user.is_authenticated():
            raise UnauthenticatedUser('user must be authenticated')
        client_id = request.REQUEST.get('client_id')
        if not client_id:
            raise InvalidRequest('no "client_id" provided')
        try:
            self.client = Client.objects.get(key=client_id)
        except Client.DoesNotExist:
            raise InvalidRequest('"client_id" does not exist')

        self.request_redirect_uri = request.REQUEST.get('redirect_uri')
        if not (self.client.redirect_uri or self.request_redirect_uri):
            raise InvalidRequest('no "redirect_uri" provided or registered')
        if self.client.redirect_uri and self.request_redirect_uri and self.client.redirect_uri != self.request_redirect_uri:
            raise InvalidRequest('"redirect_uri" does not matched the registered URI')
        redirect_uri = self.client.redirect_uri or self.request_redirect_uri
        if not absolute_http_url_re.match(redirect_uri):
            raise InvalidRequest('"redirect_uri" must be absolute')
        if urlparse(redirect_uri).fragment:
            raise InvalidRequest('"redirect_uri" must not contain a fragment')
        if settings.DJOAUTH2_SSL_ONLY and urlparse(redirect_uri).scheme != 'https':
            raise InvalidRequest('"redirect_uri" must use TLS')
        self.redirect_uri = redirect_uri
        response_type = request.REQUEST.get('response_type')
        if response_type != 'code':
            raise UnsupportedResponseType('"response_type" must be "code"')
        self.state = request.REQUEST.get('state')
        if settings.DJOAUTH2_REQUIRE_STATE and not self.state:
            raise InvalidRequest('"state" must be included')
        requested_scope_string = request.REQUEST.get('scope', '')
        if not requested_scope_string:
            raise InvalidScope('"scope" must be included')
        requested_scope_names = set(requested_scope_string.split(' '))
        self.valid_scope_objects = Scope.objects.filter(name__in=requested_scope_names)
        valid_scope_names = {scope.name for scope in self.valid_scope_objects}
        if valid_scope_names < requested_scope_names:
            raise InvalidScope(('The following scopes are invalid: {}').format((', ').join(('"{}"').format(name) for name in requested_scope_names - valid_scope_names)))

    def get_request_uri_parameters(self, as_dict=False):
        """ Return the URI parameters from a request passed to the 'validate' method

    The query parameters returned by this method **MUST** be included in the
    ``action=""`` URI of the authorization form presented to the user. This
    carries the original authorization request parameters across the request to
    show the form to the request that submits the form.

    :param as_dict: default ``False``. If ``True``, returns the parameters as a
        dictionary. If ``False``, returns the parameters as a URI-encoded
        string.
    """
        if not self.request:
            raise ValueError('request must have been passed to the "validate" method')
        return (dict if as_dict else urlencode)(self.request.REQUEST.items())

    def make_error_redirect(self, authorization_error=None):
        """ Return a Django ``HttpResponseRedirect`` describing the request failure.

    If the :py:meth:`validate` method raises an error, the authorization
    endpoint should return the result of calling this method like so:

      >>> auth_code_generator = (
      >>>     AuthorizationCodeGenerator('/oauth2/missing_redirect_uri/'))
      >>> try:
      >>>   auth_code_generator.validate(request)
      >>> except AuthorizationError as authorization_error:
      >>>   return auth_code_generator.make_error_redirect(authorization_error)

    If there is no known Client ``redirect_uri`` (because it is malformed, or
    the Client is invalid, or if the supplied ``redirect_uri`` does not match
    the regsitered value, or some other request failure) then the response will
    redirect to the ``missing_redirect_uri`` passed to the :py:meth:`__init__`
    method.

    Also used to signify user denial; call this method without passing in the
    optional ``authorization_error`` argument to return a generic
    :py:class:`AccessDenied` message.

      >>> if not user_accepted_request:
      >>>   return auth_code_generator.make_error_redirect()

    """
        if not self.redirect_uri:
            return HttpResponseRedirect(self.missing_redirect_uri)
        else:
            authorization_error = authorization_error or AccessDenied('user denied the request')
            response_params = get_error_details(authorization_error)
            if self.state is not None:
                response_params['state'] = self.state
            return HttpResponseRedirect(update_parameters(self.redirect_uri, response_params))

    def make_success_redirect(self):
        """ Return a Django ``HttpResponseRedirect`` describing the request success.

    The custom authorization endpoint should return the result of this method
    when the user grants the Client's authorization request. The request is
    assumed to have successfully been vetted by the :py:meth:`validate` method.
    """
        new_authorization_code = AuthorizationCode.objects.create(user=self.user, client=self.client, redirect_uri=self.redirect_uri if self.request_redirect_uri else None)
        new_authorization_code.scopes = self.valid_scope_objects
        new_authorization_code.save()
        response_params = {'code': new_authorization_code.value}
        if self.state is not None:
            response_params['state'] = self.state
        return HttpResponseRedirect(update_parameters(self.redirect_uri, response_params))


def make_authorization_endpoint(missing_redirect_uri, authorization_endpoint_uri, authorization_template_name):
    """ Returns a endpoint that handles OAuth authorization requests.

  The template described by ``authorization_template_name`` is rendered with a
  Django ``RequestContext`` with the following variables:

  * ``form``: a Django ``Form`` that may hold data internal to the ``djoauth2``
    application.
  * ``client``: The :py:class:`djoauth2.models.Client` requesting access to the
    user's scopes.
  * ``scopes``: A list of :py:class:`djoauth2.models.Scope`, one for each of
    the scopes requested by the client.
  * ``form_action``: The URI to which the form should be submitted -- use this
    value in the ``action=""`` attribute on a ``<form>`` element.

  :param missing_redirect_uri: a string, the URI to which to redirect the user
      when the request is made by a client without a valid redirect URI.

  :param authorization_endpoint_uri: a string, the URI of this endpoint. Used
      by the authorization form so that the form is submitted to this same
      endpoint.

  :param authorization_template_name: a string, the name of the template to
      render when handling authorization requests.

  :rtype: A view function endpoint.
  """

    @login_required
    @require_http_methods(['GET', 'POST'])
    def authorization_endpoint(request):
        auth_code_generator = AuthorizationCodeGenerator(missing_redirect_uri)
        try:
            auth_code_generator.validate(request)
        except AuthorizationError as authorization_error:
            return auth_code_generator.make_error_redirect(authorization_error)

        if request.method == 'GET':
            return render(request, authorization_template_name, {'form': Form(), 
               'client': auth_code_generator.client, 
               'scopes': auth_code_generator.valid_scope_objects, 
               'form_action': update_parameters(authorization_endpoint_uri, auth_code_generator.get_request_uri_parameters(as_dict=True))})
        if request.method == 'POST':
            form = Form(request)
            if form.is_valid() and request.POST.get('user_action') == 'Accept':
                return auth_code_generator.make_success_redirect()
            return auth_code_generator.make_error_redirect()

    return authorization_endpoint


class AuthorizationError(DJOAuthError):
    """ Base class for authorization-related errors.

  Read the specification: http://tools.ietf.org/html/rfc6749#section-4.1.2.1 .
  """
    pass


class UnauthenticatedUser(AuthorizationError):
    """ Raised when the user is not authenticated during authorization.

  Not part of the OAuth specification.
  """
    pass


class InvalidRequest(AuthorizationError):
    """ The request is missing a required parameter, includes an invalid
  parameter value, includes a parameter more than once, or is otherwise
  malformed.
  """
    error_name = 'invalid_request'


class UnauthorizedClient(AuthorizationError):
    """ The client is not authorized to request an authorization code using this
  method.
  """
    error_name = 'unauthorized_client'


class AccessDenied(AuthorizationError):
    """ The resource owner or authorization server denied the request. """
    error_name = 'access_denied'


class UnsupportedResponseType(AuthorizationError):
    """ The authorization server does not support obtaining an authorization code
  using this method.
  """
    error_name = 'unsupported_response_type'


class InvalidScope(AuthorizationError):
    """ The requested scope is invalid, unknown, or malformed. """
    error_name = 'invalid_scope'


class ServerError(AuthorizationError):
    """  The authorization server encountered an unexpected condition that
  prevented it from fulfilling the request. (This error code is needed because
  a 500 Internal Server Error HTTP status code cannot be returned to the client
  via an HTTP redirect.)
  """
    error_name = 'server_error'


class TemporarilyUnavailable(AuthorizationError):
    """ The authorization server is currently unable to handle the request due to
  a temporary overloading or maintenance of the server. (This error code is
  needed because a 503 Service Unavailable HTTP status code cannot be returned
  to the client via an HTTP redirect.) """
    error_name = 'temporarily_unavailable'