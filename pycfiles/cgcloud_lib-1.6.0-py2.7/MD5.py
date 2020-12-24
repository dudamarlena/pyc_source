# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cgcloud_Crypto/Hash/MD5.py
# Compiled at: 2016-11-22 15:21:45
"""MD5 cryptographic hash algorithm.

MD5 is specified in RFC1321_ and produces the 128 bit digest of a message.

    >>> from cgcloud_Crypto.Hash import MD5
    >>>
    >>> h = MD5.new()
    >>> h.update(b'Hello')
    >>> print h.hexdigest()

MD5 stand for Message Digest version 5, and it was invented by Rivest in 1991.

This algorithm is insecure. Do not use it for new designs.

.. _RFC1321: http://tools.ietf.org/html/rfc1321 
"""
from __future__ import nested_scopes
_revision__ = '$Id$'
__all__ = [
 'new', 'block_size', 'digest_size']
from cgcloud_Crypto.Util.py3compat import *
if sys.version_info[0] == 2 and sys.version_info[1] == 1:
    from cgcloud_Crypto.Util.py21compat import *

def __make_constructor():
    try:
        from hashlib import md5 as _hash_new
    except ImportError:
        from md5 import new as _hash_new

    h = _hash_new()
    if hasattr(h, 'new') and hasattr(h, 'name') and hasattr(h, 'digest_size') and hasattr(h, 'block_size'):
        return _hash_new
    else:
        _copy_sentinel = object()

        class _MD5(object):
            digest_size = 16
            block_size = 64
            name = 'md5'

            def __init__(self, *args):
                if args and args[0] is _copy_sentinel:
                    self._h = args[1]
                else:
                    self._h = _hash_new(*args)

            def copy(self):
                return _MD5(_copy_sentinel, self._h.copy())

            def update(self, *args):
                f = self.update = self._h.update
                f(*args)

            def digest(self):
                f = self.digest = self._h.digest
                return f()

            def hexdigest(self):
                f = self.hexdigest = self._h.hexdigest
                return f()

        _MD5.new = _MD5
        return _MD5


new = __make_constructor()
del __make_constructor
digest_size = new().digest_size
block_size = new().block_size