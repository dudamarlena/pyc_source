# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/bitwarden_simple_cli/services/SecureStorageService.py
# Compiled at: 2019-04-19 09:41:11
# Size of source mod 2**32: 1734 bytes
from base64 import b64decode, b64encode
import bitwarden_simple_cli.models.domain.SymmetricCryptoKey as SymmetricCryptoKey
import bitwarden_simple_cli.services.CryptoService as CryptoService
import bitwarden_simple_cli.services.StorageService as StorageService
from bitwarden_simple_cli.services.Tools import T
from os import environ as os_environ

class SecureStorageService:
    cryptoService: CryptoService
    storageService: StorageService

    def __init__(self, storage_service: StorageService, crypto_service: CryptoService):
        self.cryptoService = crypto_service
        self.storageService = storage_service

    def decrypt(self, enc_value) -> str:
        try:
            session_key = self._get_session_key()
            if session_key is None:
                return ''
            dec_value = self.cryptoService.decrypt_from_bytes(b64decode(enc_value), session_key)
            if dec_value is None:
                T.error('Failed to decrypt')
                return ''
            return b64encode(dec_value)
        except Exception as e:
            try:
                T.error(e)
                T.error('Decrypt error')
            finally:
                e = None
                del e

    def get(self, key: str):
        value = self.storageService.get(self._make_protected_storage_key(key))
        if value is None:
            return
        return self.decrypt(value)

    @staticmethod
    def _get_session_key():
        try:
            if os_environ.get('BW_SESSION'):
                return SymmetricCryptoKey(b64decode(os_environ['BW_SESSION']))
        except Exception as e:
            try:
                T.error(e)
                print('Session key is invalid.')
            finally:
                e = None
                del e

    @staticmethod
    def _make_protected_storage_key(key) -> str:
        return '__PROTECTED__' + key