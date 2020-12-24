# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/grpcio/grpc/_auth.py
# Compiled at: 2020-01-10 16:25:22
# Size of source mod 2**32: 2621 bytes
"""GRPCAuthMetadataPlugins for standard authentication."""
import inspect
from concurrent import futures
import grpc

def _sign_request(callback, token, error):
    metadata = (
     (
      'authorization', 'Bearer {}'.format(token)),)
    callback(metadata, error)


def _create_get_token_callback(callback):

    def get_token_callback(future):
        try:
            access_token = future.result().access_token
        except Exception as exception:
            _sign_request(callback, None, exception)
        else:
            _sign_request(callback, access_token, None)

    return get_token_callback


class GoogleCallCredentials(grpc.AuthMetadataPlugin):
    __doc__ = 'Metadata wrapper for GoogleCredentials from the oauth2client library.'

    def __init__(self, credentials):
        self._credentials = credentials
        self._pool = futures.ThreadPoolExecutor(max_workers=1)
        self._is_jwt = 'additional_claims' in inspect.getargspec(credentials.get_access_token).args

    def __call__(self, context, callback):
        if self._is_jwt:
            future = self._pool.submit((self._credentials.get_access_token),
              additional_claims={'aud': context.service_url})
        else:
            future = self._pool.submit(self._credentials.get_access_token)
        future.add_done_callback(_create_get_token_callback(callback))

    def __del__(self):
        self._pool.shutdown(wait=False)


class AccessTokenAuthMetadataPlugin(grpc.AuthMetadataPlugin):
    __doc__ = 'Metadata wrapper for raw access token credentials.'

    def __init__(self, access_token):
        self._access_token = access_token

    def __call__(self, context, callback):
        _sign_request(callback, self._access_token, None)