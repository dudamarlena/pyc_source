# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/legions/commands/more/more_commands.py
# Compiled at: 2020-05-07 10:49:55
# Size of source mod 2**32: 3804 bytes
from nubia import command, argument
from web3 import Web3
w3 = Web3()
from termcolor import cprint

@command
class Conversions:
    __doc__ = 'Conversions possible to do with Web3'

    def __init__(self) -> None:
        pass

    @command('toHex')
    @argument('value', description='value to be converted')
    def toHex(self, value: str) -> str:
        """
        Converts the input text to Hex
        """
        try:
            cprint('Hex of {}: {}'.format(value, w3.toHex(text=value)), 'green')
        except Exception as e:
            try:
                cprint('Failed to convert {}: {} '.format(value, e), 'yellow')
            finally:
                e = None
                del e

    @command('toText')
    @argument('value', description='value to be converted')
    def toText(self, value: str) -> str:
        """
        Converts the input Hex to Text
        """
        try:
            cprint('Text of {}: {}'.format(value, w3.toText(value)), 'green')
        except Exception as e:
            try:
                cprint('Failed to convert {}: {} '.format(value, e), 'yellow')
            finally:
                e = None
                del e

    @command('toBytes')
    @argument('value', description='value to be converted')
    def toBytes(self, value: str) -> str:
        """
        Converts the input to Bytes
        """
        try:
            cprint('Bytes of {}: {}'.format(value, w3.toBytes(text=value)), 'green')
        except Exception as e:
            try:
                cprint('Failed to convert {}: {} '.format(value, e), 'yellow')
            finally:
                e = None
                del e

    @command('toWei')
    @argument('value', description='value to be converted')
    @argument('currency', description='type of the input, unit of currency')
    def toWei(self, value: float, currency: str='ether') -> str:
        """
        Converts the input to Wei 
        """
        try:
            cprint('toWei {}: {}'.format(value, w3.toWei(value, currency)), 'green')
        except Exception as e:
            try:
                cprint('Failed to convert {} to {}: {}'.format(value, currency, e), 'yellow')
            finally:
                e = None
                del e

    @command('fromWei')
    @argument('value', description='value to be converted')
    @argument('currency', description='type of the output, unit of currency')
    def fromWei(self, value: int, currency: str='ether') -> str:
        """
        Converts the input to ether (or specified currency)
        """
        try:
            cprint('fromWei {} to {}: {:18f}'.format(value, currency, w3.fromWei(value, currency)), 'green')
        except Exception as e:
            try:
                cprint('Failed to convert {} to {}: {}'.format(value, currency, e), 'yellow')
            finally:
                e = None
                del e

    @command('toChecksumAddress')
    @argument('value', description='value to be converted')
    def toChecksumAddress(self, value: str) -> str:
        """
        Converts the input to Checksum Address
        """
        try:
            cprint('toChecksumAddress of {}: {}'.format(value, w3.toChecksumAddress(value)), 'green')
        except Exception as e:
            try:
                cprint('Failed to toChecksumAddress {}: {}'.format(value, e), 'yellow')
            finally:
                e = None
                del e

    @command('keccak')
    @argument('value', description='value to be hashed')
    def keccak(self, value: str) -> str:
        """
        keccak hash of the input
        """
        try:
            cprint('keccak of {}: {}'.format(value, w3.toHex(w3.keccak(text=value))), 'green')
        except Exception as e:
            try:
                cprint('Failed to get keccak of {}: {}'.format(value, e), 'yellow')
            finally:
                e = None
                del e