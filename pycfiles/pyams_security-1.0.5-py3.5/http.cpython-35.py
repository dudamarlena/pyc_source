# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_security/plugin/http.py
# Compiled at: 2020-02-21 07:52:38
# Size of source mod 2**32: 2541 bytes
"""PyAMS_security.plugin.http module

This module defines an HTTP authentication module.
"""
import base64, re
from pyams_security.credential import Credentials
from pyams_security.interfaces import ICredentialsPlugin
from pyams_utils.registry import utility_config
from pyams_utils.wsgi import wsgi_environ_cache
__docformat__ = 'restructuredtext'
from pyams_security import _
ENVKEY_PARSED_CREDENTIALS = 'pyams_security.http.basic.credentials'
CUSTOM_LOGIN = re.compile('^{(.*)}\\.?(.*)')

@utility_config(name='http', provides=ICredentialsPlugin)
class HttpBasicCredentialsPlugin:
    __doc__ = 'HTTP basic credentials plug-in\n\n    This credential plug-in is mainly used by automation processes using\n    XML-RPC or JSON-RPC requests launched from batch scripts.\n\n    Copied from pyramid_httpauth package.\n    '
    prefix = 'http'
    title = _('HTTP Basic credentials')
    enabled = True

    @wsgi_environ_cache(ENVKEY_PARSED_CREDENTIALS)
    def extract_credentials(self, request, **kwargs):
        """Extract login/password credentials from given request"""
        auth = request.headers.get('Authorization')
        if not auth:
            return
        try:
            scheme, params = auth.split(' ', 1)
            if scheme.lower() != 'basic':
                return
            else:
                token_bytes = base64.b64decode(params.strip())
                try:
                    token = token_bytes.decode('utf-8')
                except UnicodeDecodeError:
                    token = token_bytes.decode('latin-1')

                login, password = token.split(':', 1)
                if login.startswith('{'):
                    principal_id = CUSTOM_LOGIN.sub('\\1:\\2', login)
                    prefix, login = principal_id.split(':')
                else:
                    principal_id = login
                return Credentials(self.prefix, principal_id, login=login, password=password)
        except (ValueError, TypeError):
            return