# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bitcoin/script/redeem/multisig.py
# Compiled at: 2017-07-08 11:42:23
# Size of source mod 2**32: 2815 bytes
"""
Models a ReedemScript for a multisignature Address
"""
from .. import pay
from .model import RedeemScript
from ...field import OP_CMS, ScriptData, get_op_code_n

class MultiSig(RedeemScript):
    __doc__ = '\n    Models a Multisignature script\n\n    Attributes:\n        _keys_needed (int): number of keys needed to unlock the script funds\n            if no keys needed specified, the resulting script will have no\n            needed keys specified, meaning that can be used for\n            TimeLockedScripts, for example\n        _keys_total (int): number of keys in the multisig script\n            if not specified, will be the same as keys_needed\n            if neither keys needed are specified or total keys, an error will\n            be triggered\n    '
    __slots__ = ['_keys_needed', '_keys_total', '_public_keys']

    def __init__(self, needed=None, total=None):
        super().__init__(None)
        if not needed is not None:
            assert total is not None, 'You must specify ' + 'at least the needed keys or the total keys'
        self._keys_needed = needed
        self._keys_total = total if total is not None else needed
        self._public_keys = []

    def add_public_key(self, public_key):
        """
        Adds a public key to t he addressess list in order to have one more
        address to allow the payment

        Args:
            public_key (bytes): public key to append to the list of public keys
        """
        assert len(self._public_keys) < self._keys_total, 'Too many addressess'
        self._public_keys.append(public_key)

    def remove_public_key(self, public_key):
        """
        Removes a public key from the addresses list

        Args:
            public_key (bytes): public key to remove of the list of public keys
        """
        assert public_key in self._public_keys, 'Pubkey not in list'
        self._public_keys.remove(public_key)

    def _build(self):
        """
        Creates the script with the opcodes and the data necessary:
            OP_M <pk_n> .. <pk_1> OP_N OP_CMS
        """
        assert len(self._public_keys) == self._keys_total, 'The MultiSig ' + 'redeem script needs exactly %d pubkeys' % self._keys_total
        self._data = []
        if self._keys_needed is not None:
            self._data.append(get_op_code_n(self._keys_needed))
        for pk in self._public_keys:
            self._data.append(ScriptData(pk))

        self._data.append(get_op_code_n(self._keys_total))
        self._data.append(OP_CMS)

    @property
    def pay_script(self):
        return pay.MultiSig(self)