# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/peterdowns/Desktop/djoauth2/djoauth2/decorators.py
# Compiled at: 2013-11-22 18:12:08
from django.utils.functional import wraps
from djoauth2.access_token import AccessTokenAuthenticator

def oauth_scope(*scope_names):
    """ Return a decorator that restricts requests to those authorized with
  a certain scope or scopes.

  For example, to restrict access to a given endpoint like this:

  .. code-block:: python

      @require_login
      def secret_attribute_endpoint(request, *args, **kwargs):
        user = request.user
        return HttpResponse(json.dumps({
            'super_secret_attribute' : user.super_secret_attribute
          })

  ...just add the decorator and an additional argument to the function's
  signature:

  .. code-block:: python

      @oauth_scope('foo', 'bar')
      def secret_attribute_endpoint(access_token, request, *args, **kwargs):
        # Because of the decorator, the function is guaranteed to only be run
        # if the request includes proper access to the 'foo' and 'bar'
        # scopes.
        user = access_token.user
        return HttpResponse(json.dumps({
            'super_secret_attribute' : user.super_secret_attribute
          })

  The first argument to the wrapped endpoint will now be an
  :py:class:`djoauth2.models.AccessToken` object. The second argument will be
  the original Django ``HttpRequest``, and all other parameters included in the
  requests (due to URL-matching or any other method) will follow.

  We **strongly recommend** that you use this decorator to protect your API
  endpoints instead of manually instantiating a
  djoauth2.access_token.AccessTokenAuthenticator object.
  """
    authenticator = AccessTokenAuthenticator(required_scope_names=scope_names)

    def scope_decorator(view_func):

        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            access_token, error_response_arguments = authenticator.validate(request)
            if not access_token:
                return authenticator.make_error_response(*error_response_arguments)
            return view_func(access_token, request, *args, **kwargs)

        return wrapper

    return scope_decorator