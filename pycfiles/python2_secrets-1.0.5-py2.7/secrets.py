# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/secrets/secrets.py
# Compiled at: 2018-09-18 07:49:25
"""Generate cryptographically strong pseudo-random numbers suitable for

managing secrets such as account authentication, tokens, and similar.

See PEP 506 for more information.

https://www.python.org/dev/peps/pep-0506/

"""
__all__ = [
 'choice', 'randbelow', 'randbits', 'SystemRandom',
 'token_bytes', 'token_hex', 'token_urlsafe',
 'compare_digest']
import os, sys
from random import SystemRandom
import base64, binascii
if sys.version_info >= (2, 7, 7):
    from hmac import compare_digest
else:

    def compare_digest(a, b):
        """Compatibility compare_digest method for python < 2.7.
        This method is NOT cryptographically secure and may be subject to
        timing attacks, see https://docs.python.org/2/library/hmac.html
        """
        return a == b


_sysrand = SystemRandom()
randbits = _sysrand.getrandbits
choice = _sysrand.choice

def randbelow(exclusive_upper_bound):
    """Return a random int in the range [0, n)."""
    if exclusive_upper_bound <= 0:
        raise ValueError('Upper bound must be positive.')
    return _sysrand._randbelow(exclusive_upper_bound)


DEFAULT_ENTROPY = 32

def token_bytes(nbytes=None):
    r"""Return a random byte string containing *nbytes* bytes.

    If *nbytes* is ``None`` or not supplied, a reasonable

    default is used.

    >>> token_bytes(16)  #doctest:+SKIP

    b'\xebr\x17D*t\xae\xd4\xe3S\xb6\xe2\xebP1\x8b'

    """
    if nbytes is None:
        nbytes = DEFAULT_ENTROPY
    return os.urandom(nbytes)


def token_hex(nbytes=None):
    """Return a random text string, in hexadecimal.

    The string has *nbytes* random bytes, each byte converted to two

    hex digits.  If *nbytes* is ``None`` or not supplied, a reasonable

    default is used.

    >>> token_hex(16)  #doctest:+SKIP

    'f9bf78b9a18ce6d46a0cd2b0b86df9da'

    """
    return binascii.hexlify(token_bytes(nbytes)).decode('ascii')


def token_urlsafe(nbytes=None):
    """Return a random URL-safe text string, in Base64 encoding.

    The string has *nbytes* random bytes.  If *nbytes* is ``None``

    or not supplied, a reasonable default is used.

    >>> token_urlsafe(16)  #doctest:+SKIP

    'Drmhze6EPcv0fN_81Bj-nA'

    """
    tok = token_bytes(nbytes)
    return base64.urlsafe_b64encode(tok).rstrip('=').decode('ascii')