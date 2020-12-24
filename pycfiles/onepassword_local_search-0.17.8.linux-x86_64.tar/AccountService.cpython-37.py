# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/onepassword_local_search/services/AccountService.py
# Compiled at: 2019-05-24 16:38:48
# Size of source mod 2**32: 3921 bytes
import onepassword_local_search.services.StorageService as StorageService
import onepassword_local_search.services.ConfigFileService as ConfigFileService
import onepassword_local_search.services.CryptoService as CryptoService
import onepassword_local_search.services.SecondaryCryptoService as SecondaryCryptoService
import onepassword_local_search.exceptions.ManagedException as ManagedException
from sys import stderr
from os import environ as os_environ

class AccountService:
    accounts: []
    existing_accounts: []
    disable_session_caching: bool
    storageService: StorageService
    configFileService: ConfigFileService
    cryptoServices = {}
    cryptoServices: {}

    def __init__(self, storage_service: StorageService, config_file_service: ConfigFileService, disable_session_caching=False):
        self.storageService = storage_service
        self.configFileService = config_file_service
        self.existing_accounts = self.configFileService.get_accounts()
        self.accounts = self.get_available_accounts()
        self.available_vaults = self.get_available_vaults()
        self.available_vaults_id = self.get_available_vaults_id()
        self.disable_session_caching = disable_session_caching

    def get_available_accounts(self):
        accounts = []
        for account in self.existing_accounts:
            if not os_environ.get('OP_SESSION_' + account['shorthand']):
                continue
            account_id = self.storageService.get_account_id_from_user_uuid(account['userUUID'])
            if account_id:
                account['id'] = account_id
                accounts.append(account)

        return accounts

    def get_available_accounts_id(self):
        return [str(account['id']) for account in self.accounts]

    def get_available_vaults(self):
        return self.storageService.get_vaults_owned_by_accounts(self.get_available_accounts_id())

    def get_available_vaults_id(self):
        if self.available_vaults:
            if len(self.available_vaults) > 0:
                return [vault['id'] for vault in self.available_vaults]
        return []

    def set_crypto_services(self):
        services = {}
        not_logged_accounts = []
        try:
            for account in self.accounts:
                if self.is_main_account(account):
                    crypto_class = CryptoService
                else:
                    crypto_class = SecondaryCryptoService
                try:
                    services[account['id']] = crypto_class(self.storageService, self.configFileService, account['id'])
                except Exception:
                    not_logged_accounts.append(account)

            if len(not_logged_accounts) > 0:
                raise ManagedException('Not authenticated')
        except Exception:
            for account in not_logged_accounts:
                if account['shorthand'] == 'my':
                    over = 'your personal account'
                else:
                    over = 'the team %s' % account['shorthand']
                print(('You are not authenticated over "%s"' % over), file=stderr)

            raise

        return services

    def get_main_crypto_service(self):
        return self.cryptoServices['1']

    def get_decryptor(self, vaultId):
        if self.cryptoServices == {}:
            self.cryptoServices = self.set_crypto_services()
        for vault in self.available_vaults:
            if vaultId == vault['id']:
                account_id = vault['account_id']
                break
        else:
            raise ManagedException('Unable to find proper decryptor for vault %s' % vaultId)

        if account_id in self.cryptoServices.keys():
            return self.cryptoServices[account_id]
        raise ManagedException('Unable to find proper decryptor for vault %s' % vaultId)

    def is_main_account(self, account):
        return account['id'] == 1