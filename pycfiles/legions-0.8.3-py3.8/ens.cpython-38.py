# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/legions/commands/more/ens.py
# Compiled at: 2020-05-07 10:49:55
# Size of source mod 2**32: 1785 bytes
from ens import ENS as _ens
from web3 import Web3
from termcolor import cprint
from nubia import command, argument
from legions.commands.commands import w3

@command
class ens:
    __doc__ = 'Ethereum name system'

    def __init__(self) -> None:
        self.ns = _ens.fromWeb3(w3)

    @command('toName')
    @argument('value', description='address to be converted to a name')
    def toName(self, value: str) -> str:
        """
        Converts an address to a ens name
        """
        try:
            cprint('Name of {}: {}'.format(value, self.ns.name(value)))
        except Exception as e:
            try:
                cprint('Failed to convert {}: {}'.format(value, e), 'yellow')
            finally:
                e = None
                del e

    @command('toAddress')
    @argument('value', description='name to be converted to an address')
    def toAddress(self, value: str) -> str:
        """
        Converts a ENS name to an address
        """
        try:
            cprint('Address of {}: {}'.format(value, self.ns.address(value)))
        except Exception as e:
            try:
                cprint('Failed to convert {}: {}'.format(value, e), 'yellow')
            finally:
                e = None
                del e

    @command('info')
    @argument('name', description='name to get information about')
    def info(self, name: str) -> str:
        """
        Get info about an ENS name
        """
        cprint("Information about '{}'".format(name))
        cprint('Valid name: {}'.format(self.ns.is_valid_name(name)))
        if self.ns.is_valid_name(name):
            cprint('Namehash: {}'.format(self.ns.namehash(name).hex()))
            resolver = self.ns.resolver(name)
            if resolver is not None:
                cprint('Resolver: {}'.format(resolver.address))
                cprint('Owner: {}'.format(self.ns.owner(name)))
            else:
                cprint('Is not registered')