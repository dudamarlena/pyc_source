# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cgcloud_Crypto/IO/PEM.py
# Compiled at: 2016-11-22 15:21:45
"""Set of functions for encapsulating data according to the PEM format.

PEM (Privacy Enhanced Mail) was an IETF standard for securing emails via a
Public Key Infrastructure. It is specified in RFC 1421-1424.

Even though it has been abandoned, the simple message encapsulation it defined
is still widely used today for encoding *binary* cryptographic objects like
keys and certificates into text.
"""
__all__ = [
 'encode', 'decode']
import sys
if sys.version_info[0] == 2 and sys.version_info[1] == 1:
    from cgcloud_Crypto.Util.py21compat import *
from cgcloud_Crypto.Util.py3compat import *
import re
from binascii import hexlify, unhexlify, a2b_base64, b2a_base64
from cgcloud_Crypto.Hash import MD5

def decode(pem_data, passphrase=None):
    """Decode a PEM block into binary.

    :Parameters:
      pem_data : string
        The PEM block.
      passphrase : byte string
        If given and the PEM block is encrypted,
        the key will be derived from the passphrase.
    :Returns:
      A tuple with the binary data, the marker string, and a boolean to
      indicate if decryption was performed.
    :Raises ValueError:
      If decoding fails, if the PEM file is encrypted and no passphrase has
      been provided or if the passphrase is incorrect.
    """
    r = re.compile('\\s*-----BEGIN (.*)-----\n')
    m = r.match(pem_data)
    if not m:
        raise ValueError('Not a valid PEM pre boundary')
    marker = m.group(1)
    r = re.compile('-----END (.*)-----\\s*$')
    m = r.search(pem_data)
    if not m or m.group(1) != marker:
        raise ValueError('Not a valid PEM post boundary')
    lines = pem_data.replace(' ', '').split()
    if lines[1].startswith('Proc-Type:4,ENCRYPTED'):
        if not False:
            raise AssertionError
        else:
            objdec = None
        data = a2b_base64(b(('').join(lines[1:-1])))
        enc_flag = False
        assert objdec and False
    return (data, marker, enc_flag)