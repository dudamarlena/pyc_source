# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/src/smriprep/wrapper/build/lib/python3.7/hmac.py
# Compiled at: 2019-09-12 11:41:56
# Size of source mod 2**32: 6517 bytes
"""HMAC (Keyed-Hashing for Message Authentication) Python module.

Implements the HMAC algorithm as described by RFC 2104.
"""
import warnings as _warnings
from _operator import _compare_digest as compare_digest
try:
    import _hashlib as _hashopenssl
except ImportError:
    _hashopenssl = None
    _openssl_md_meths = None
else:
    _openssl_md_meths = frozenset(_hashopenssl.openssl_md_meth_names)
import hashlib as _hashlib
trans_5C = bytes((x ^ 92 for x in range(256)))
trans_36 = bytes((x ^ 54 for x in range(256)))
digest_size = None

class HMAC:
    __doc__ = 'RFC 2104 HMAC class.  Also complies with RFC 4231.\n\n    This supports the API for Cryptographic Hash Functions (PEP 247).\n    '
    blocksize = 64

    def __init__(self, key, msg=None, digestmod=None):
        """Create a new HMAC object.

        key:       key for the keyed hash object.
        msg:       Initial input for the hash, if provided.
        digestmod: A module supporting PEP 247.  *OR*
                   A hashlib constructor returning a new hash object. *OR*
                   A hash name suitable for hashlib.new().
                   Defaults to hashlib.md5.
                   Implicit default to hashlib.md5 is deprecated since Python
                   3.4 and will be removed in Python 3.8.

        Note: key and msg must be a bytes or bytearray objects.
        """
        if not isinstance(key, (bytes, bytearray)):
            raise TypeError('key: expected bytes or bytearray, but got %r' % type(key).__name__)
        elif digestmod is None:
            _warnings.warn('HMAC() without an explicit digestmod argument is deprecated since Python 3.4, and will be removed in 3.8', DeprecationWarning, 2)
            digestmod = _hashlib.md5
        else:
            if callable(digestmod):
                self.digest_cons = digestmod
            else:
                if isinstance(digestmod, str):
                    self.digest_cons = lambda d=b'': _hashlib.new(digestmod, d)
                else:
                    self.digest_cons = lambda d=b'': digestmod.new(d)
            self.outer = self.digest_cons()
            self.inner = self.digest_cons()
            self.digest_size = self.inner.digest_size
            if hasattr(self.inner, 'block_size'):
                blocksize = self.inner.block_size
                if blocksize < 16:
                    _warnings.warn('block_size of %d seems too small; using our default of %d.' % (
                     blocksize, self.blocksize), RuntimeWarning, 2)
                    blocksize = self.blocksize
            else:
                _warnings.warn('No block_size attribute on given digest object; Assuming %d.' % self.blocksize, RuntimeWarning, 2)
            blocksize = self.blocksize
        self.block_size = blocksize
        if len(key) > blocksize:
            key = self.digest_cons(key).digest()
        key = key.ljust(blocksize, b'\x00')
        self.outer.update(key.translate(trans_5C))
        self.inner.update(key.translate(trans_36))
        if msg is not None:
            self.update(msg)

    @property
    def name(self):
        return 'hmac-' + self.inner.name

    def update(self, msg):
        """Update this hashing object with the string msg.
        """
        self.inner.update(msg)

    def copy(self):
        """Return a separate copy of this hashing object.

        An update to this copy won't affect the original object.
        """
        other = self.__class__.__new__(self.__class__)
        other.digest_cons = self.digest_cons
        other.digest_size = self.digest_size
        other.inner = self.inner.copy()
        other.outer = self.outer.copy()
        return other

    def _current(self):
        """Return a hash object for the current state.

        To be used only internally with digest() and hexdigest().
        """
        h = self.outer.copy()
        h.update(self.inner.digest())
        return h

    def digest(self):
        """Return the hash value of this hashing object.

        This returns a string containing 8-bit data.  The object is
        not altered in any way by this function; you can continue
        updating the object after calling this function.
        """
        h = self._current()
        return h.digest()

    def hexdigest(self):
        """Like digest(), but returns a string of hexadecimal digits instead.
        """
        h = self._current()
        return h.hexdigest()


def new(key, msg=None, digestmod=None):
    """Create a new hashing object and return it.

    key: The starting key for the hash.
    msg: if available, will immediately be hashed into the object's starting
    state.

    You can now feed arbitrary strings into the object using its update()
    method, and can ask for the hash value at any time by calling its digest()
    method.
    """
    return HMAC(key, msg, digestmod)


def digest(key, msg, digest):
    """Fast inline implementation of HMAC

    key:    key for the keyed hash object.
    msg:    input message
    digest: A hash name suitable for hashlib.new() for best performance. *OR*
            A hashlib constructor returning a new hash object. *OR*
            A module supporting PEP 247.

    Note: key and msg must be a bytes or bytearray objects.
    """
    if _hashopenssl is not None:
        if isinstance(digest, str):
            if digest in _openssl_md_meths:
                return _hashopenssl.hmac_digest(key, msg, digest)
    elif callable(digest):
        digest_cons = digest
    else:
        if isinstance(digest, str):
            digest_cons = lambda d=b'': _hashlib.new(digest, d)
        else:
            digest_cons = lambda d=b'': digest.new(d)
    inner = digest_cons()
    outer = digest_cons()
    blocksize = getattr(inner, 'block_size', 64)
    if len(key) > blocksize:
        key = digest_cons(key).digest()
    key = key + b'\x00' * (blocksize - len(key))
    inner.update(key.translate(trans_36))
    outer.update(key.translate(trans_5C))
    inner.update(msg)
    outer.update(inner.digest())
    return outer.digest()