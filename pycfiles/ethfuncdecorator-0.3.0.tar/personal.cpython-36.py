# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/q3/1b9f00755fngs2554s60x4_h0000gn/T/pycharm-packaging/web3/web3/personal.py
# Compiled at: 2018-05-28 04:44:24
# Size of source mod 2**32: 1799 bytes
from web3.module import Module

class Personal(Module):
    __doc__ = '\n    https://github.com/ethereum/go-ethereum/wiki/Management-APIs#personal\n    '

    def importRawKey(self, private_key, passphrase):
        return self.web3.manager.request_blocking('personal_importRawKey', [
         private_key, passphrase])

    def newAccount(self, password):
        return self.web3.manager.request_blocking('personal_newAccount', [password])

    @property
    def listAccounts(self):
        return self.web3.manager.request_blocking('personal_listAccounts', [])

    def sendTransaction(self, transaction, passphrase):
        return self.web3.manager.request_blocking('personal_sendTransaction', [
         transaction, passphrase])

    def lockAccount(self, account):
        return self.web3.manager.request_blocking('personal_lockAccount', [
         account])

    def unlockAccount(self, account, passphrase, duration=None):
        try:
            return self.web3.manager.request_blocking('personal_unlockAccount', [
             account, passphrase, duration])
        except ValueError as err:
            if 'could not decrypt' in str(err):
                return False
            raise

    def sign(self, message, signer, passphrase):
        return self.web3.manager.request_blocking('personal_sign', [
         message, signer, passphrase])

    def ecRecover(self, message, signature):
        return self.web3.manager.request_blocking('personal_ecRecover', [
         message, signature])