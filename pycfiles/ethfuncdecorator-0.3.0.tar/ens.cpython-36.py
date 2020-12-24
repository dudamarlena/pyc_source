# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/q3/1b9f00755fngs2554s60x4_h0000gn/T/pycharm-packaging/web3/web3/utils/ens.py
# Compiled at: 2018-05-28 04:44:24
# Size of source mod 2**32: 1554 bytes
from contextlib import contextmanager
from eth_utils import is_0x_prefixed, is_hex, is_hex_address
from ens import ENS
from web3.exceptions import NameNotFound

def is_ens_name(value):
    if not isinstance(value, str):
        return False
    else:
        if is_hex_address(value):
            return False
        if is_0x_prefixed(value):
            if is_hex(value):
                return False
        return ENS.is_valid_name(value)


def validate_name_has_address(ens, name):
    addr = ens.address(name, guess_tld=False)
    if addr:
        return addr
    raise NameNotFound('Could not find address for name %r' % name)


class StaticENS:

    def __init__(self, name_addr_pairs):
        self.registry = dict(name_addr_pairs)

    def address(self, name, guess_tld=True):
        assert not guess_tld
        return self.registry.get(name, None)


@contextmanager
def ens_addresses(w3, name_addr_pairs):
    original_ens = w3.ens
    w3.ens = StaticENS(name_addr_pairs)
    yield
    w3.ens = original_ens


@contextmanager
def contract_ens_addresses(contract, name_addr_pairs):
    """
    Use this context manager to temporarily resolve name/address pairs
    supplied as the argument. For example:

    with contract_ens_addresses(mycontract, [('resolve-as-1s.eth', '0x111...111')]):
        # any contract call or transaction in here would only resolve the above ENS pair
    """
    with ens_addresses(contract.web3, name_addr_pairs):
        yield