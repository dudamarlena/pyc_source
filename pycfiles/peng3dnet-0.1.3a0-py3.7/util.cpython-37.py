# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/peng3dnet/util.py
# Compiled at: 2017-06-26 13:11:20
# Size of source mod 2**32: 3054 bytes
from . import errors

def parse_address(addr, default_port=8080):
    r"""
    Parses an IP Address into a tuple of ``(addr,port)``\ .
    
    If the address does not contain an explicitly specified port, the value given with ``default_port`` is used.
    
    Note that currently only IPv4 addresses are supported, but IPv6 support may be added in the future.
    If an IPv6 Address is detected, a :py:exc:`~peng3dnet.errors.UnsupportedAddressError` will be raised.
    
    Additionally, the port returned is checked for plausibility, e.g. an integer in range 0-65535.
    If the port is invalid in any way, a :py:exc:`~peng3dnet.errors.InvalidPortError` will be raised.
    """
    addr = str(addr)
    addrs = addr.split(':')
    if len(addrs) == 1:
        addr = addrs[0]
        port = default_port
    else:
        if len(addrs) == 2:
            addr = addrs[0]
            try:
                port = int(addrs[1])
            except Exception:
                raise errors.InvalidPortError('Port %s is not an integer' % addrs[1])

        else:
            raise errors.UnsupportedAddressError('Address appears to be an IPv6 address, currently not supported')
    if not isinstance(port, int):
        raise errors.InvalidPortError('Port must be an integer')
    else:
        if port < 0:
            raise errors.InvalidPortError('Port may not be less than zero')
        else:
            if port > 65535:
                raise errors.InvalidPortError('Port may not be higher than 65535')
    return (
     addr, port)


def normalize_addr_socketstyle(addr, default_port=8080):
    """
    Normalizes the given address to a 2-tuple as accepted by the :py:mod:`socket` module.
    
    Currently accepts a 2-tuple and IPv4 addresses in string format.
    
    If the address does not contain a port, the ``default_port`` will be used.
    
    Note that this function will pass through any exceptions raised by parsing functions it calls.
    """
    if len(addr) == 2:
        return addr
    return parse_address(addr, default_port)


def normalize_addr_formatted(addr):
    r"""
    Normalizes the given address to a string like ``127.0.0.1``\ .
    
    This method is currently not implemented.
    """
    raise NotImplementedError('not yet implemented')