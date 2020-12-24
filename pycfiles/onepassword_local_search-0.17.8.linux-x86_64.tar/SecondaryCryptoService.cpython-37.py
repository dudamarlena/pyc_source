# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/onepassword_local_search/services/SecondaryCryptoService.py
# Compiled at: 2019-05-24 16:38:48
# Size of source mod 2**32: 2159 bytes
import onepassword_local_search.services.StorageService as StorageService
import onepassword_local_search.services.ConfigFileService as ConfigFileService
import onepassword_local_search.models.Cipher as Cipher
from onepassword_local_search.lib.optestlib import aes_decrypt, get_binary_from_string, rsa_decrypt, determine_session_file_path_from_session_key
from os import environ as os_environ, path as os_path
from json import loads as json_loads
from glob import glob as glob_glob
import sys
import onepassword_local_search.services.CryptoService as CryptoService

class SecondaryCryptoService(CryptoService):
    mainCryptoService: CryptoService

    def __init__(self, storage_service, config_file_service, account_id):
        super().__init__(storage_service, config_file_service, account_id)
        self.set_main_crypto_service()

    def _get_base_keys(self):
        self.sessionKey = self._get_session_key()
        self.encryptedSessionPrivateKey = self._get_encrypted_session_key()
        self.sessionPrivateKey = json_loads(self.decrypt(self.sessionKey, self.encryptedSessionPrivateKey))
        self.encyptedSymmetricyKey = Cipher(self._get_encrypted_symmetric_key())
        self.symmetricKey = json_loads(self.decrypt(self.sessionPrivateKey['encodedMuk'], self.encyptedSymmetricyKey))
        self.encryptedAccountKey = Cipher(self._get_encrypted_account_key())
        self.accountKey = json_loads(self.decrypt(self.mainCryptoService.symmetricKey['k'], self.encryptedAccountKey))
        self.encryptedPrivateKey = Cipher(self._get_encrypted_private_key())
        self.privateKeyRaw = self.decrypt(self.symmetricKey['k'], self.encryptedPrivateKey).decode('utf-8')
        self.privateKey = json_loads(self.privateKeyRaw)

    def set_main_crypto_service(self):
        self.mainCryptoService = CryptoService(self.storageService, self.configFileService, self.storageService.get_account_id_from_user_uuid(self.get_main_user_uuid()))
        self.mainCryptoService._get_base_keys()

    def get_main_user_uuid(self):
        return self.storageService.get_main_user_uuid()