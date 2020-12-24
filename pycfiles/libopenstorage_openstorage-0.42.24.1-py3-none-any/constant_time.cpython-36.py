# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/cryptography/cryptography/hazmat/primitives/constant_time.py
# Compiled at: 2020-01-10 16:25:38
# Size of source mod 2**32: 1139 bytes
from __future__ import absolute_import, division, print_function
import hmac, warnings
from cryptography import utils
from cryptography.hazmat.bindings._constant_time import lib
if hasattr(hmac, 'compare_digest'):

    def bytes_eq(a, b):
        if not isinstance(a, bytes) or not isinstance(b, bytes):
            raise TypeError('a and b must be bytes.')
        return hmac.compare_digest(a, b)


else:
    warnings.warn('Support for your Python version is deprecated. The next version of cryptography will remove support. Please upgrade to a release (2.7.7+) that supports hmac.compare_digest as soon as possible.', utils.PersistentlyDeprecated2018)

    def bytes_eq(a, b):
        if not isinstance(a, bytes) or not isinstance(b, bytes):
            raise TypeError('a and b must be bytes.')
        return lib.Cryptography_constant_time_bytes_eq(a, len(a), b, len(b)) == 1