# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/webapi/errors.py
# Compiled at: 2019-06-12 01:17:17
from __future__ import unicode_literals

class WebAPIError(object):
    """
    An API error, containing an error code and human readable message.
    """

    def __init__(self, code, msg, http_status=400, headers={}):
        self.code = code
        self.msg = msg
        self.http_status = http_status
        self.headers = headers

    def __repr__(self):
        return b'<API Error %d, HTTP %d: %s>' % (self.code, self.http_status,
         self.msg)

    def with_overrides(self, msg=None, headers=None):
        """Overrides the default message and/or headers for an error."""
        if headers is None:
            headers = self.headers
        return WebAPIError(self.code, msg or self.msg, self.http_status, headers)

    def with_message(self, msg):
        """
        Overrides the default message for a WebAPIError with something
        more context specific.

        Example:
        return ENABLE_EXTENSION_FAILED.with_message('some error message')
        """
        return self.with_overrides(msg)


class WebAPITokenGenerationError(Exception):
    """An error generating a Web API token."""
    pass


def _get_auth_headers(request):
    from djblets.webapi.auth.backends import get_auth_backends
    headers = {}
    www_auth_schemes = []
    for auth_backend_cls in get_auth_backends():
        auth_backend = auth_backend_cls()
        if auth_backend.www_auth_scheme:
            www_auth_schemes.append(auth_backend.www_auth_scheme)
        headers.update(auth_backend.get_auth_headers(request))

    if www_auth_schemes:
        headers[b'WWW-Authenticate'] = (b', ').join(www_auth_schemes)
    return headers


NO_ERROR = WebAPIError(0, b'If you see this, yell at the developers')
SERVICE_NOT_CONFIGURED = WebAPIError(1, b'The web service has not yet been configured', http_status=503)
DOES_NOT_EXIST = WebAPIError(100, b'Object does not exist', http_status=404)
PERMISSION_DENIED = WebAPIError(101, b"You don't have permission for this", http_status=403)
INVALID_ATTRIBUTE = WebAPIError(102, b'Invalid attribute', http_status=400)
NOT_LOGGED_IN = WebAPIError(103, b'You are not logged in', http_status=401, headers=_get_auth_headers)
LOGIN_FAILED = WebAPIError(104, b'The username or password was not correct', http_status=401, headers=_get_auth_headers)
INVALID_FORM_DATA = WebAPIError(105, b'One or more fields had errors', http_status=400)
MISSING_ATTRIBUTE = WebAPIError(106, b'Missing value for the attribute', http_status=400)
ENABLE_EXTENSION_FAILED = WebAPIError(107, b'There was a problem enabling the extension', http_status=500)
DISABLE_EXTENSION_FAILED = WebAPIError(108, b'There was a problem disabling the extension', http_status=500)
EXTENSION_INSTALLED = WebAPIError(109, b'This extension has already been installed.', http_status=409)
INSTALL_EXTENSION_FAILED = WebAPIError(110, b'An error occurred while installing the extension', http_status=409)
DUPLICATE_ITEM = WebAPIError(111, b'An entry for this item or its unique key(s) already exists', http_status=409)
OAUTH_MISSING_SCOPE_ERROR = WebAPIError(112, b'Your OAuth2 token lacks the necessary scopes for this request.', http_status=403)
OAUTH_ACCESS_DENIED_ERROR = WebAPIError(113, b'OAuth2 token access for this resource is prohibited.', http_status=403)
RATE_LIMIT_EXCEEDED = WebAPIError(114, b'API rate limit has been exceeded.', http_status=429)