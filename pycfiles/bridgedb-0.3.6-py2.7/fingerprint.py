# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bridgedb/parse/fingerprint.py
# Compiled at: 2015-11-05 10:40:17
"""
.. py:module:: bridgedb.parse.fingerprint
    :synopsis: Parsers for Tor Bridge fingerprints.

.. todo: This module is very small; it could possibly be combined with another
    module, e.g. :mod:`bridgedb.parse.descriptors`.

bridgedb.parse.fingerprint
============================

Utility functions for converting between various relay fingerprint formats,
and checking their validity.

::

 toHex - Convert a fingerprint from its binary representation to hexadecimal.
 fromHex - Convert a fingerprint from hexadecimal to binary.
 isValidFingerprint - Validate a fingerprint.
..
"""
import binascii, logging
HEX_FINGERPRINT_LEN = 40
toHex = binascii.b2a_hex
fromHex = binascii.a2b_hex

def isValidFingerprint(fingerprint):
    """Determine if a Tor relay fingerprint is valid.

    :param str fingerprint: The hex-encoded hash digest of the relay's
        public identity key, a.k.a. its fingerprint.
    :rtype: bool
    :returns: ``True`` if the **fingerprint** was valid, ``False`` otherwise.
    """
    try:
        if len(fingerprint) != HEX_FINGERPRINT_LEN:
            raise ValueError('Fingerprint has incorrect length: %r' % repr(fingerprint))
        fromHex(fingerprint)
    except (TypeError, ValueError):
        logging.debug('Invalid hex fingerprint: %r' % repr(fingerprint))
    else:
        return True

    return False