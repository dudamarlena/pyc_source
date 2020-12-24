# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/webapi/auth/backends/basic.py
# Compiled at: 2019-06-12 01:17:17
"""An authentication backend for HTTP Basic Auth."""
from __future__ import unicode_literals
import logging
from djblets.webapi.auth.backends.base import WebAPIAuthBackend
logger = logging.getLogger(__name__)

class WebAPIBasicAuthBackend(WebAPIAuthBackend):
    """Handles HTTP Basic Authentication for the web API."""
    www_auth_scheme = b'Basic realm="Web API"'

    def get_credentials(self, request):
        parts = request.META[b'HTTP_AUTHORIZATION'].split(b' ')
        realm = parts[0]
        if realm != b'Basic':
            return
        else:
            try:
                encoded_auth = parts[1]
                username, password = encoded_auth.decode(b'base64').split(b':', 1)
            except Exception:
                logger.warning(b'Failed to parse HTTP_AUTHORIZATION header %s', request.META[b'HTTP_AUTHORIZATION'], exc_info=True, extra={b'request': request})
                return

            return {b'username': username, 
               b'password': password}