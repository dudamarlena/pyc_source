# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/bitwarden_simple_cli/services/CipherService.py
# Compiled at: 2019-04-19 09:41:11
# Size of source mod 2**32: 932 bytes
import bitwarden_simple_cli.models.domain.Cipher as Cipher
import bitwarden_simple_cli.services.StorageService as StorageService
import bitwarden_simple_cli.services.UserService as UserService
Keys = dict(ciphersPrefix='ciphers_',
  localData='sitesLocalData',
  neverDomains='neverDomains')

class CipherService:
    storageService = None
    userService = None

    def __init__(self, storage_service: StorageService, user_service: UserService):
        self.storageService = storage_service
        self.userService = user_service

    def get(self, uuid: str):
        user_id = self.userService.get_user_id()
        local_data = self.storageService.get(Keys['localData'])
        ciphers = self.storageService.get(Keys['ciphersPrefix'] + user_id)
        if ciphers is None or uuid not in ciphers:
            return
        return Cipher(ciphers[uuid], False, local_data[uuid] if local_data else None)