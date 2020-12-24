# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/schevo/store/utils.py
# Compiled at: 2007-03-21 14:34:41
"""$URL: svn+ssh://svn.mems-exchange.org/repos/trunk/durus/utils.py $
$Id: utils.py 1475 2005-12-01 17:36:40Z mscott $
"""
from schevo.lib import optimize
import struct

def format_oid(oid):
    """(oid:str) -> str
    Returns a nice representation of an 8-byte oid.
    """
    return str(oid and u64(oid))


def p64(v):
    """Pack an integer or long into a 8-byte string"""
    return struct.pack('>Q', v)


def u64(v):
    """Unpack an 8-byte string into a 64-bit long integer."""
    return struct.unpack('>Q', v)[0]


def p32(v):
    """Pack an integer or long into a 4-byte string"""
    return struct.pack('>L', v)


def u32(v):
    """Unpack an 8-byte string into a 32-bit long integer."""
    return struct.unpack('>L', v)[0]


import sys
optimize.bind_all(sys.modules[__name__])