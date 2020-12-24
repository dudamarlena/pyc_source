# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gamerocket/util/crypto.py
# Compiled at: 2013-08-19 08:43:10
from urllib import urlencode, quote
import base64, hashlib

class Crypto(object):

    def __init__(self, config):
        self.config = config
        self.environment = self.config.environment

    def sign(self, method, url, parameters, secretKey):
        base_string = self._build_base_string(method, url, parameters)
        return self._sign(base_string, secretKey)

    def _build_base_string(self, method, url, parameters):
        parameters = self.config.sort_dict(parameters)
        base_string = method + '&' + quote(url.lower(), '') + '&'
        qs = ''
        if parameters != {}:
            qs = urlencode(parameters)
        base_string = base_string + quote(qs)
        return base_string

    def _sign(self, base_string, secretKey):
        to_sha256 = hashlib.sha256()
        to_sha256.update(base_string + secretKey)
        string_sha256 = to_sha256.hexdigest()
        string_base64 = base64.b64encode(string_sha256)
        return string_base64