# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/fedservice/keybundle.py
# Compiled at: 2019-05-29 15:00:52
# Size of source mod 2**32: 2381 bytes
import json, logging
from cryptojwt import key_bundle
from cryptojwt.jws.jws import factory
from cryptojwt.key_jar import KeyJar
logger = logging.getLogger(__name__)

class KeyBundle(key_bundle.KeyBundle):
    __doc__ = '\n    Extended :py:class:`oidcmsg.key_bundle.KeyBundle` class that supports\n    signed JWKS uris.\n    '

    def __init__(self, keys=None, source='', cache_time=300, verify_ssl=True, file_format='jwk', keytype='RSA', keyusage=None, verify_keys=None):
        super(KeyBundle, self).__init__(keys=keys, source=source, cache_time=cache_time,
          verify_ssl=verify_ssl,
          fileformat=file_format,
          keytype=keytype,
          keyusage=keyusage)
        if verify_keys is not None:
            if isinstance(verify_keys, KeyJar):
                self.verify_keys = verify_keys
            else:
                self.verify_keys = KeyJar()
                self.verify_keys.import_jwks(verify_keys, '')

    def _parse_remote_response(self, response):
        """
        Parse simple JWKS or signed JWKS from the HTTP response.

        :param response: HTTP response from the 'jwks_uri' or 'signed_jwks_uri'
            endpoint
        :return: response parsed as JSON or None
        """
        try:
            if response.headers['Content-Type'] == 'application/json':
                logger.debug('Loaded JWKS: %s from %s' % (response.text, self.source))
                try:
                    return json.loads(response.text)
                except ValueError:
                    return

            else:
                if response.headers['Content-Type'] == 'application/jwt':
                    logger.debug('Signed JWKS: %s from %s' % (response.text, self.source))
                    _jws = factory(response.text)
                    _resp = _jws.verify_compact((response.text),
                      keys=(self.verify_keys.get_signing_key()))
                    return _resp
                logger.error('Wrong content type: {}'.format(response.headers['Content-Type']))
                raise ValueError('Content-type mismatch')
        except KeyError:
            pass