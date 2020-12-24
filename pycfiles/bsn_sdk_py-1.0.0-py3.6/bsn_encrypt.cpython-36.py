# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\common\bsn_encrypt.py
# Compiled at: 2020-04-23 03:19:47
# Size of source mod 2**32: 2975 bytes
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import load_pem_private_key, Encoding, PrivateFormat
from cryptography.x509 import load_pem_x509_certificate, NameOID
from hfc.util.crypto.crypto import Ecies, ecies, CURVE_P_256_Size, SHA2
from bsn_sdk_py.until.bsn_logger import log_debug, log_info

class BsnCrypto:

    def __init__(self, private_key_path, pubilc_key_path):
        self.private_key_data = self._load_private_key_data(private_key_path)
        self.pubilc_key_data = self._load_pubilc_key_data(pubilc_key_path)

    def sign(self, message):
        pass

    def verify(self, message, signature):
        pass


class ECDSA(BsnCrypto):

    def __init__(self, private_key_path, pubilc_key_path):
        super().__init__(private_key_path, pubilc_key_path)

    def _load_private_key_data(self, user_private_cert_path):
        with open(user_private_cert_path, 'rb') as (fp):
            user_private_key = fp.read()
        skey = load_pem_private_key(user_private_key, password=None, backend=(default_backend()))
        return skey

    def _load_pubilc_key_data(self, app_public_cert_path):
        with open(app_public_cert_path, 'rb') as (fp):
            pubilc_key_data = fp.read()
        cert = load_pem_x509_certificate(pubilc_key_data, default_backend())
        public_key = cert.public_key()
        return public_key

    def sign(self, message):
        log_info('ECDSA 加签')
        signature = Ecies(CURVE_P_256_Size, SHA2).sign(private_key=(self.private_key_data), message=(message.encode('utf-8')))
        return base64.b64encode(signature)

    def verify(self, message, signature):
        log_info('ECDSA 验签')
        mac = signature
        verify_results = Ecies().verify(public_key=(self.pubilc_key_data), message=(message.encode('utf-8')), signature=(base64.b64decode(mac)))
        return verify_results


class SM2(BsnCrypto):

    def __init__(self, private_key_path, pubilc_key_path):
        super().__init__(private_key_path, pubilc_key_path)

    def _load_private_key_data(self, user_private_cert_path):
        pass

    def _load_pubilc_key_data(self, app_public_cert_path):
        pass

    def sign(self, message):
        log_info('SM2 加签')

    def verify(self, message, signature):
        log_info('SM2 验签')


if __name__ == '__main__':
    s = SM2()