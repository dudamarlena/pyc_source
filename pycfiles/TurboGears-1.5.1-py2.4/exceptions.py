# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\turbogears\identity\exceptions.py
# Compiled at: 2011-07-08 11:09:24
"""Identity management exceptions."""
__all__ = [
 'IdentityConfigurationException', 'IdentityException', 'IdentityFailure', 'IdentityManagementNotEnabledException', 'RequestRequiredException', 'get_failure_url', 'get_identity_errors', 'set_identity_errors']
from cherrypy import request, response, HTTPRedirect, InternalRedirect
import turbogears
from turbogears import config

def set_identity_errors(errors):
    """Save the identity errors in the CherryPy request and WSGI environment."""
    request.identity_errors = request.wsgi_environ['identity.errors'] = isinstance(errors, basestring) and [errors] or list(errors)


def get_identity_errors():
    """Get the identity errors from the CherryPy request or WSGI environment."""
    return getattr(request, 'identity_errors', request.wsgi_environ.get('identity.errors', []))


def get_failure_url(errors=None):
    """Get the identity failure URL from the configuration setting."""
    url = config.get('identity.failure_url')
    if callable(url):
        url = url(errors)
    if url is None:
        msg = 'Missing URL for identity failure. Please fix this in app.cfg.'
        raise IdentityConfigurationException(msg)
    return url


class IdentityException(Exception):
    """Base class for all Identity exceptions."""
    __module__ = __name__


class RequestRequiredException(IdentityException):
    """No request present.

    An attempt was made to use a facility of Identity that requires the
    presence of an HTTP request.

    """
    __module__ = __name__

    def __str__(self):
        return self.args and self.args[0] or 'An attempt was made to use a facility of the TurboGears Identity Management framework that relies on an HTTP request outside of a request.'


class IdentityManagementNotEnabledException(IdentityException):
    """User forgot to enable Identity management."""
    __module__ = __name__

    def __str__(self):
        return self.args and self.args[0] or "An attempt was made to use a facility of the TurboGears Identity Management framework, but identity management hasn't been enabled in the config file (via identity.on)."


class IdentityConfigurationException(IdentityException):
    """Incorrect configuration.

    Exception thrown when the Identity management system hasn't been configured
    correctly. Mostly, when failure_url is not specified.

    """
    __module__ = __name__

    def __str__(self):
        return self.args and self.args[0] or 'Unknown Identity configuration error.'


class IdentityFailure(InternalRedirect, IdentityException):
    """Identity failure.

    Exception thrown when an access control check fails.

    """
    __module__ = __name__

    def __init__(self, errors):
        """Set up identity errors on the request and get URL from config."""
        set_identity_errors(errors)
        url = get_failure_url(errors)
        if config.get('identity.force_external_redirect', False):
            try:
                params = request.original_params
            except AttributeError:
                params = request.params
            else:
                params['forward_url'] = request.path_info
                url = turbogears.url(url, params)
                raise HTTPRedirect(url)
        else:
            env = request.wsgi_environ
            if config.get('identity.http_basic_auth', False):
                env['identity.status'] = '401 Unauthorized'
                env['identity.auth_realm'] = 'Basic realm="%s"' % config.get('identity.http_auth_realm', 'TurboGears')
            else:
                env['identity.status'] = '403 Forbidden'
            env['identity.path_info'] = request.path_info
            env['identity.params'] = request.params
            InternalRedirect.__init__(self, url)