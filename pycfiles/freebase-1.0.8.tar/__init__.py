# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/andrew/hello/freebase/__init__.py
# Compiled at: 2009-06-18 13:50:01
import sys
from freebase.api.session import HTTPMetawebSession
import sandbox
__all__ = [
 'HTTPMetawebSession', 'sandbox']
_base = HTTPMetawebSession('freebase.com')
self = sys.modules[__name__]
for funcname in dir(_base):
    if not funcname.startswith('_'):
        func = getattr(_base, funcname)
        if callable(func):
            setattr(self, funcname, func)
            __all__.append(funcname)

del self
del funcname
del func