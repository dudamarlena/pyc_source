# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/column/api/manager/credential_manager.py
# Compiled at: 2017-08-02 01:06:09
import logging
from column import utils
LOG = logging.getLogger(__name__)

class CredentialManager(object):
    """Column Credential Manager class

    The Credential Manager layer is to support additional logic which is needed
    to update and get credential.

    """

    def get_credential(self, cred):
        return utils.vault_decrypt(cred['value'])

    def update_credential(self, cred):
        return utils.vault_encrypt(cred['value'])