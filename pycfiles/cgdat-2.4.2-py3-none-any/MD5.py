# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cgcloud_Crypto/Hash/MD5.py
# Compiled at: 2016-11-22 15:21:45
__doc__ = "MD5 cryptographic hash algorithm.\n\nMD5 is specified in RFC1321_ and produces the 128 bit digest of a message.\n\n    >>> from cgcloud_Crypto.Hash import MD5\n    >>>\n    >>> h = MD5.new()\n    >>> h.update(b'Hello')\n    >>> print h.hexdigest()\n\nMD5 stand for Message Digest version 5, and it was invented by Rivest in 1991.\n\nThis algorithm is insecure. Do not use it for new designs.\n\n.. _RFC1321: http://tools.ietf.org/html/rfc1321 \n"
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