# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/blockcypher/crypto.py
# Compiled at: 2020-01-07 12:17:40
from bitcoin import encode, changebase, binascii, bin_to_b58check
import re

def script_to_address(script, vbyte=0):
    """
    Like script_to_address but supports altcoins
    Copied 2015-10-02 from https://github.com/mflaxman/pybitcointools/blob/faf56c53148989ea390238c3c4541a6ae1d601f5/bitcoin/transaction.py#L224-L236
    """
    if re.match('^[0-9a-fA-F]*$', script):
        script = binascii.unhexlify(script)
    if script[:3] == b'v\xa9\x14' and script[-2:] == b'\x88\xac' and len(script) == 25:
        return bin_to_b58check(script[3:-2], vbyte)
    else:
        if vbyte in (111, 196):
            scripthash_byte = 196
        else:
            scripthash_byte = vbyte
        return bin_to_b58check(script[2:-1], scripthash_byte)