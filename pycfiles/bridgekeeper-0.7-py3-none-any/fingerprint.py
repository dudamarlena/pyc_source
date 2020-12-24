# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/bridgedb/parse/fingerprint.py
# Compiled at: 2015-11-05 10:40:17
__doc__ = '\n.. py:module:: bridgedb.parse.fingerprint\n    :synopsis: Parsers for Tor Bridge fingerprints.\n\n.. todo: This module is very small; it could possibly be combined with another\n    module, e.g. :mod:`bridgedb.parse.descriptors`.\n\nbridgedb.parse.fingerprint\n============================\n\nUtility functions for converting between various relay fingerprint formats,\nand checking their validity.\n\n::\n\n toHex - Convert a fingerprint from its binary representation to hexadecimal.\n fromHex - Convert a fingerprint from hexadecimal to binary.\n isValidFingerprint - Validate a fingerprint.\n..\n'
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