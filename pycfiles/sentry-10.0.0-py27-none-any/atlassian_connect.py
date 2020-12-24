# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/integrations/atlassian_connect.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import hashlib, jwt
from sentry.models import Integration
from sentry.utils.http import percent_encode
__all__ = [
 'AtlassianConnectValidationError', 'get_query_hash', 'get_integration_from_request']

class AtlassianConnectValidationError(Exception):
    pass


def get_query_hash(uri, method, query_params=None):
    uri = uri.rstrip('/')
    method = method.upper()
    if query_params is None:
        query_params = {}
    sorted_query = []
    for k, v in sorted(query_params.items()):
        if k != 'jwt':
            if isinstance(v, list):
                param_val = (',').join([ percent_encode(val) for val in v ])
            else:
                param_val = percent_encode(v)
            sorted_query.append('%s=%s' % (percent_encode(k), param_val))

    query_string = '%s&%s&%s' % (method, uri, ('&').join(sorted_query))
    return hashlib.sha256(query_string.encode('utf8')).hexdigest()


def get_integration_from_jwt(token, path, provider, query_params, method='GET'):
    if token is None:
        raise AtlassianConnectValidationError('No token parameter')
    decoded = jwt.decode(token, verify=False)
    issuer = decoded['iss']
    try:
        integration = Integration.objects.get(provider=provider, external_id=issuer)
    except Integration.DoesNotExist:
        raise AtlassianConnectValidationError('No integration found')

    options = {}
    if provider == 'bitbucket':
        options = {'verify_aud': False}
    decoded_verified = jwt.decode(token, integration.metadata['shared_secret'], options=options)
    qsh = get_query_hash(path, method, query_params)
    if qsh != decoded_verified['qsh']:
        raise AtlassianConnectValidationError('Query hash mismatch')
    return integration


def get_integration_from_request(request, provider):
    return get_integration_from_jwt(request.GET.get('jwt'), request.path, provider, request.GET)