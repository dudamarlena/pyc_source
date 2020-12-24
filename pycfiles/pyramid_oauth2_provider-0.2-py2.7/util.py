# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/pyramid_oauth2_provider/util.py
# Compiled at: 2013-02-09 19:59:16
import base64, logging
from pyramid.threadlocal import get_current_registry
log = logging.getLogger('pyramid_oauth2_provider.util')

def oauth2_settings(key=None, default=None):
    settings = get_current_registry().settings
    if key:
        value = settings.get('oauth2_provider.%s' % key, default)
        if value == 'true':
            return True
        if value == 'false':
            return False
        return value
    else:
        return dict((x.split('.', 1)[1], y) for x, y in settings.iteritems() if x.startswith('oauth2_provider.'))


def getClientCredentials(request):
    if 'Authorization' in request.headers:
        auth = request.headers.get('Authorization')
    else:
        if 'authorization' in request.headers:
            auth = request.headers.get('authorization')
        else:
            log.debug('no authorization header found')
            return False
        if not auth.lower().startswith('bearer') and not auth.lower().startswith('basic'):
            log.debug('authorization header not of type bearer or basic: %s' % auth.lower())
            return False
        parts = auth.split()
        if len(parts) != 2:
            return False
    token_type = parts[0].lower()
    token = base64.b64decode(parts[1])
    if token_type == 'basic':
        client_id, client_secret = token.split(':')
        request.client_id = client_id
        request.client_secret = client_secret
    return (token_type, token)