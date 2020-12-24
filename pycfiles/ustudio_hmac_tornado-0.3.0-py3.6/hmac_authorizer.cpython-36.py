# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hmacauth/server/hmac_authorizer.py
# Compiled at: 2017-07-26 11:26:21
# Size of source mod 2**32: 1276 bytes
import hmac, logging, functools
from tornado.web import HTTPError
from hmacauth.digest import generate_digest

def hmac_authorized(method):

    @functools.wraps(method)
    def hmac_authorized_wrapper(handler, *args, **kwargs):
        authorization = handler.request.headers.get('Authorization', '').split(' ')
        if len(authorization) != 3:
            logging.info('Invalid Authorization header {}'.format(authorization))
            raise HTTPError(401)
        algorithm, key, provided_digest = authorization
        if algorithm != 'USTUDIO-HMAC-V2':
            logging.info('Invalid algorithm {}'.format(algorithm))
            raise HTTPError(401)
        secret = handler.get_hmac_secret(key)
        if secret is None:
            logging.info('Invalid HMAC key {}'.format(key))
            raise HTTPError(401)
        expected_digest = generate_digest(secret, handler.request.method, handler.request.path, handler.request.query, handler.request.body)
        if not hmac.compare_digest(expected_digest, provided_digest):
            logging.info('Invalid HMAC digest {}'.format(provided_digest))
            raise HTTPError(401)
        return method(handler, *args, **kwargs)

    return hmac_authorized_wrapper