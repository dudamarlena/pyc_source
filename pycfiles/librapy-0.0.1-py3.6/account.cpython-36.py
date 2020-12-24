# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/librapy/account.py
# Compiled at: 2019-09-06 14:27:58
# Size of source mod 2**32: 941 bytes
"""
Collection of all the components associated with an account.
"""

class Account:

    def __init__(self, address, signing_key):
        self.address = address
        self.signing_key = signing_key
        self.balance = 0
        self.sequence_number = 0

    def __repr__(self):
        return 'Account(\n\taddress: {}\n\tbalance: {}\n\tsequence_number: {}\n\tpublic_key: {}\n)'.format(self.address, self.balance, self.sequence_number, self.signing_key.verify_key.encode().hex())

    def get_address(self):
        return self.address

    def get_signing_key(self):
        return self.signing_key

    def update(self, account_resource):
        self.balance = account_resource.balance
        self.sequence_number = account_resource.sequence_number