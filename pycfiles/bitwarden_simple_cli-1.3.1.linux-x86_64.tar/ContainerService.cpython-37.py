# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/bitwarden_simple_cli/services/ContainerService.py
# Compiled at: 2019-04-19 09:41:11
# Size of source mod 2**32: 1087 bytes
import bitwarden_simple_cli.services.CryptoService as CryptoService
import bitwarden_simple_cli.services.SecureStorageService as SecureStorageService

class ContainerService:

    class __ContainerService:
        services = dict()

        def add_service(self, service):
            self.services[type(service).__name__] = service

        def get_crypto_service(self) -> CryptoService.CryptoService:
            return self.services['CryptoService']

        def get_secure_storage_service(self) -> SecureStorageService.SecureStorageService:
            return self.services['SecureStorageService']

        def get_service(self, service):
            return self.services[service]

    instance = None

    @classmethod
    def __new__(cls, arg=None):
        if not ContainerService.instance:
            ContainerService.instance = ContainerService._ContainerService__ContainerService()
        return ContainerService.instance

    def __getattr__(self, item):
        return getattr(self.instance, item)

    def __setattr__(self, key, value):
        return setattr(self.instance, key, value)