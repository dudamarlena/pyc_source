# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/bitwarden_simple_cli/Bitwarden.py
# Compiled at: 2019-04-19 09:41:11
# Size of source mod 2**32: 2493 bytes
from os import environ
from sys import exit, stdout, stderr
import bitwarden_simple_cli.services.ContainerService as ContainerService
import bitwarden_simple_cli.services.CryptoService as CryptoService
import bitwarden_simple_cli.services.SecureStorageService as SecureStorageService
import bitwarden_simple_cli.services.StorageService as StorageService
import bitwarden_simple_cli.services.UserService as UserService
import bitwarden_simple_cli.services.CipherService as CipherService
import bitwarden_simple_cli.exceptions.ManagedException as ManagedException

class Bitwarden:
    containerService: ContainerService
    cryptoService: CryptoService
    secureStorageService: SecureStorageService
    storageService: StorageService

    def __init__(self):
        self.storageService = StorageService()
        self.cryptoService = CryptoService(self.storageService)
        self.secureStorageService = SecureStorageService(self.storageService, self.cryptoService)
        self.userService = UserService(self.storageService)
        self.cipherService = CipherService(self.storageService, self.userService)
        self.containerService = ContainerService()
        self.containerService.add_service(self.cryptoService)
        self.containerService.add_service(self.secureStorageService)

    def _exit_if_no_session(self):
        if not environ.get('BW_SESSION'):
            print('Environement variable BW_SESSION is not set.')
            exit(1)
        if not self.cryptoService.has_key():
            print('Vault is locked.')
            exit(1)

    def get(self, uuid, field):
        self._exit_if_no_session()
        cipher = self.cipherService.get(uuid)
        if cipher is None:
            raise ManagedException('Unable to find entry with id: ' + uuid)
        decrypted_value = cipher.decrypt_field(field)
        if type(decrypted_value).__name__ == 'bytes':
            print((str(decrypted_value, 'utf-8')), end='')
            return decrypted_value
        if type(decrypted_value).__name__ == 'list':
            for item in decrypted_value:
                print(str(item, 'utf-8'))

            return decrypted_value
        print(decrypted_value, file=stderr)

    def list(self):
        self._exit_if_no_session()
        ciphers = self.storageService.list_ciphers(self.userService.get_user_id())
        for cipher in ciphers:
            print(cipher['id'] + ' ' + str(cipher['name'].decrypt(cipher['org_id']), 'utf-8'))