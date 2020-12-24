# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cgcloud_Crypto/PublicKey/_slowmath.py
# Compiled at: 2016-11-22 15:21:45
"""Pure Python implementation of the RSA-related portions of Crypto.PublicKey._fastmath."""
__revision__ = '$Id$'
__all__ = [
 'rsa_construct']
import sys
if sys.version_info[0] == 2 and sys.version_info[1] == 1:
    from cgcloud_Crypto.Util.py21compat import *
from cgcloud_Crypto.Util.number import inverse

class error(Exception):
    pass


class _RSAKey(object):

    def has_private(self):
        return hasattr(self, 'd')


def rsa_construct(n, e, d=None, p=None, q=None, u=None):
    """Construct an RSAKey object"""
    assert isinstance(n, long)
    assert isinstance(e, long)
    assert isinstance(d, (long, type(None)))
    assert isinstance(p, (long, type(None)))
    assert isinstance(q, (long, type(None)))
    assert isinstance(u, (long, type(None)))
    obj = _RSAKey()
    obj.n = n
    obj.e = e
    if d is None:
        return obj
    else:
        obj.d = d
        if p is not None and q is not None:
            obj.p = p
            obj.q = q
        else:
            assert False
        if u is not None:
            obj.u = u
        else:
            obj.u = inverse(obj.p, obj.q)
        return obj