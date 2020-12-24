# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/substrate/data/lib/substrate/agar/auth.py
# Compiled at: 2012-02-03 19:38:43
"""
The ``agar.auth`` module contains classes, functions, and decorators to help secure a `webapp2.Requesthandler`_.
"""
from functools import wraps
from agar.config import Config

def authenticate_abort_403(handler):
    """
    An authenticate function for use with the :py:func:`~agar.auth.authentication_required` decorator. Simply aborts
    the call with a status code of ``403``.
    """
    handler.abort(403)


class AuthConfig(Config):
    """
    :py:class:`~agar.config.Config` settings for the ``agar.auth`` library.
    Settings are under the ``agar_auth`` namespace.

    The following settings (and defaults) are provided::

        agar_auth_AUTHENTICATION_PROPERTY = 'user'
        agar_auth_DEFAULT_AUTHENTICATE_FUNCTION = agar.auth.authenticate_abort_403

    To override ``agar.auth`` settings, define values in the ``appengine_config.py`` file in the root of your project.
    """
    _prefix = 'agar_auth'
    AUTHENTICATION_PROPERTY = 'user'
    DEFAULT_AUTHENTICATE_FUNCTION = authenticate_abort_403


config = AuthConfig.get_config()

def authentication_required(authenticate=None, require_https=False):
    """
    A decorator to authenticate a `webapp2.RequestHandler`_.
    The decorator will assign the return value from the ``authenticate`` function to the request ``user`` attribute
    (or any re-configured name via the config :py:attr:`~agar.auth.AuthConfig.AUTHENTICATION_PROPERTY`), that is
    passed to the decorated handler. The ``authenticate`` function can call `webapp2.abort`_ if there was a problem
    authenticating the call.

    :param authenticate: The authentication function. It should take a single `webapp2.RequestHandler`_ argument, and
        return a value representing the authentication or call `webapp2.abort`_ to short circuit the decorated
        handler. The type of the returned value can be anything, but it should be a type that your
        `webapp2.RequestHandler`_ expects. If ``None``, the configured
        :py:attr:`~agar.auth.AuthConfig.DEFAULT_AUTHENTICATE_FUNCTION` will be used.
    :param require_https: If ``True``, this will enforce that a request was made via HTTPS, otherwise a ``403`` response
        will be returned.
    """
    if authenticate is None:
        authenticate = config.DEFAULT_AUTHENTICATE_FUNCTION

    def decorator(request_method):

        @wraps(request_method)
        def wrapped(self, *args, **kwargs):
            if require_https:
                import urlparse
                from agar.env import on_server
                scheme, netloc, path, query, fragment = urlparse.urlsplit(self.request.url)
                if on_server and scheme and scheme.lower() != 'https':
                    self.abort(403)
            setattr(self.request, config.AUTHENTICATION_PROPERTY, authenticate(self))
            request_method(self, *args, **kwargs)

        return wrapped

    return decorator


def https_authentication_required(authenticate=None):
    """
    A decorator to authenticate a secure request to a `webapp2.RequestHandler`_. Simply calls the
    :py:func:`~agar.auth.authentication_required` decorator with ``require_https=True``.

    :param authenticate: The authentication function passed to the :py:func:`~agar.auth.authentication_required`
        decorator.
    """
    return authentication_required(authenticate=authenticate, require_https=True)