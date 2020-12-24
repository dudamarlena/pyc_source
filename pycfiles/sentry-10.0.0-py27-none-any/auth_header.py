# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/byk/Documents/Projects/sentry/sentry/src/sentry/testutils/helpers/auth_header.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
__all__ = ('get_auth_header', )

def get_auth_header(client, api_key=None, secret_key=None, version=None):
    if version is None:
        version = '6'
    header = [('sentry_client', client), ('sentry_version', version)]
    if api_key:
        header.append(('sentry_key', api_key))
    if secret_key:
        header.append(('sentry_secret', secret_key))
    return 'Sentry %s' % (', ').join('%s=%s' % (k, v) for k, v in header)