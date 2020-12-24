# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bitcoin/tx/sign.py
# Compiled at: 2017-07-08 11:42:23
# Size of source mod 2**32: 5201 bytes
"""
Provides a signable transaction, with methods to create a pseudo-transaction to
sign
"""
from enum import Enum
import copy
from .model import BasicTx
from .. import script
from ..field.general import U4BLEInt
from ..crypto import ecdsa
from ..crypto.hash import double_sha256

class HashTypes(Enum):
    __doc__ = '\n    Hashtypes available to create signable transactions as specified in:\n    https://en.bitcoin.it/wiki/OP_CHECKSIG\n    '
    all = b'\x01'
    none = b'\x02'
    single = b'\x03'
    anyonecanpay = b'\x80'


DEFAULT_HASHTYPE = HashTypes.all

class SignableTx(BasicTx):
    __doc__ = '\n    Defines a transaction that can be signed, providing methods to create a\n    pseudo-transaction that will be signed using ECDSA algorithms\n    '

    def signable_tx(self, input_num, script_pubkey, hashtype=DEFAULT_HASHTYPE):
        """
        Given an input that requires to be signed, the pubkey script that the
        input refers to, and the hashtype to use to create the signable tx,
        creates a copy of the present transaction and returns a signable copy
        with all inputs and outputs treated according to the hashtype passed
        and with the given input script changed to the pubkey script given

        Source:
        https://en.bitcoin.it/wiki/OP_CHECKSIG
        https://github.com/vbuterin/pybitcointools/blob/master/bitcoin/transaction.py

        Args:
            input_num (int): number of input to change it's script
            you can also provide the input object and we'll search for its num
            script_pubkey (script.pubkey): script to set in the input
            hashtype (HashType item): hashtype to use. Default will be used if
            empty
        """
        assert len(self.inputs), "There aren't any inputs to sign"
        from ..io.input import TxInput
        if isinstance(input_num, TxInput):
            try:
                input_num = self.inputs.index(input_num)
            except ValueError:
                raise ValueError('The input passed has not been found')

        assert isinstance(input_num, int), 'Input must be a number'
        assert input_num >= 0 and input_num < len(self.inputs), 'Input number\n        does not match any input (%d is not 0 <= num < %d)' % (
         input_num, len(self.inputs))
        assert isinstance(hashtype, HashTypes), 'The hashtype must be a '
        signable_tx = copy.deepcopy(self)
        for tx_in in signable_tx.inputs:
            tx_in.script.input = tx_in
            tx_in.script = script.ScriptSig()

        signable_tx.inputs[input_num].script = script_pubkey
        if hashtype == HashTypes.none:
            signable_tx.outputs = []
        else:
            if hashtype == HashTypes.single:
                signable_tx.outputs = signable_tx.outputs[:len(signable_tx.inputs)]
                for out in signable_tx.outputs[:len(signable_tx.inputs) - 1]:
                    out.value = 18446744073709551615
                    out.script = script.pubkey.ScriptPubKey()

            elif hashtype == HashTypes.anyonecanpay:
                signable_tx.inputs = [
                 signable_tx.inputs[input_num]]
        return signable_tx

    def signable_hash(self, hashtype=DEFAULT_HASHTYPE):
        """
        Returns the hash needed to perform signatures given the hashtype that
        will be used

        Args:
            hashtype (HashType item): hashtype to use. Default will be used if
            empty
        """
        hashtype_field = U4BLEInt(int.from_bytes(hashtype.value, 'big'))
        signable_bytes = self.serialize() + hashtype_field.serialize()
        return double_sha256(signable_bytes)

    def sign(self, key, input_num, script_pubkey, hashtype=DEFAULT_HASHTYPE):
        """
        Signs the current transaction for the given input number, by generating
        a signable transaction using the _signable_tx method with the same
        arguments and then performing the signature using the private key
        given

        Args:
            key (bytes): private key to sign as a bytes object
            input_num (int): number of input to change it's script
            script_pubkey (script.pubkey): script to set in the input
            hashtype (HashType item): hashtype to use. Default will be used if
            empty

        Returns:
            bytes: bytes object containing the signature
        """
        signable_tx = self.signable_tx(input_num, script_pubkey, hashtype)
        return ecdsa.der_sign(signable_tx.signable_hash(), key) + hashtype.value