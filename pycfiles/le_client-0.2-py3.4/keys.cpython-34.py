# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/le_client/keys.py
# Compiled at: 2016-07-21 12:15:56
# Size of source mod 2**32: 4036 bytes
import urllib.request, urllib.parse, urllib.error, hashlib, binascii, json, re, abc
from .utils import openssl, b64

class KeyFile(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def as_jwk(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def sign(self, nonce, payload):
        raise NotImplementedError()

    def thumbprint(self):
        jwk_json = json.dumps(self.as_jwk(), sort_keys=True, separators=(',', ':'))
        return b64(hashlib.sha256(jwk_json.encode('utf8')).digest())


class LocalKeyFile(KeyFile, metaclass=abc.ABCMeta):

    def __init__(self, filename):
        self.filename = filename

    @abc.abstractproperty
    def alg(self):
        raise NotImplementedError()

    def sign(self, nonce, payload):
        jwk = self.as_jwk()
        payload64 = b64(json.dumps(payload).encode('utf8'))
        protected64 = b64(json.dumps({'alg': self.alg, 
         'jwk': jwk, 
         'nonce': nonce}).encode('utf-8'))
        data = '{}.{}'.format(protected64, payload64).encode('ascii')
        out = openssl('dgst', '-sha256', '-sign', self.filename, stdin=data)
        out = out[4:4 + out[3]][-32:] + out[4 + out[3] + 2:4 + out[3] + 3 + out[(4 + out[3] + 1)]][-32:]
        return {'protected': protected64, 
         'payload': payload64, 
         'signature': b64(out)}


class ECKeyFile(LocalKeyFile):

    @property
    def alg(self):
        return 'ES256'

    def as_jwk(self):
        dump = openssl('ec', '-in', self.filename, '-noout', '-text').decode('utf-8')
        pub_hex = binascii.unhexlify(re.sub('(\\s|:)', '', re.search('pub:\\s*\\n\\s+04:([a-f0-9\\:\\s]+?)\\nASN1 OID: prime256v1\\n', dump, re.MULTILINE | re.DOTALL).group(1)))
        return {'kty': 'EC', 
         'crv': 'P-256', 
         'x': b64(pub_hex[:32]), 
         'y': b64(pub_hex[32:])}


class RemoteKey(KeyFile):

    def __init__(self, url, credentials=None, handlers=None, opener=None):
        self.url = url
        if opener is not None:
            if credentials is not None or handlers is not None:
                raise ValueError("Can't use `opener` with other kwargs")
            self.opener = opener
        else:
            all_handlers = []
            if handlers is not None:
                for handler in handlers:
                    all_handlers.append(handler)

            if credentials is not None:
                passwords = urllib.request.HTTPPasswordMgrWithDefaultRealm()
                passwords.add_password(None, url, *credentials)
                auth_handler = urllib.request.HTTPBasicAuthHandler(passwords)
                all_handlers.append(auth_handler)
            self.opener = urllib.request.build_opener(*all_handlers)

    def as_jwk(self):
        with self.opener.open(self.url) as (f):
            assert f.status == 200
            return json.loads(f.read().decode('utf-8'))

    def sign(self, nonce, payload):
        data = json.dumps(payload).encode('utf-8')
        url = '{}?nonce={}'.format(self.url, urllib.parse.quote(nonce))
        with self.opener.open(url, data) as (f):
            assert f.status == 200
            return json.loads(f.read().decode('utf-8'))