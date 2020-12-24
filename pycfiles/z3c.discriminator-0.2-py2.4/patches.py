# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.11.1-i386/egg/z3c/discriminator/patches.py
# Compiled at: 2007-11-26 11:27:16
import zope.interface.adapter, zope.configuration.fields
from z3c.discriminator import discriminator
_register = zope.interface.adapter.BaseAdapterRegistry.register

def register(self, required, provided, name, factory):
    """This method wraps ``factory`` so it's discriminator-aware
    if one or more ``required`` interfaces are designated as
    discriminators."""
    drequired = [ hasattr(r, '__discriminated__') for r in required ]
    if factory is None or len(drequired) == 0:
        return _register(self, required, provided, name, factory)

    def _factory(*args):
        _ = [ provided for (provided, implemented) in zip(args, tuple(required) + (None, ) * (len(args) - len(required))) if not hasattr(implemented, '__discriminated__') ]
        return factory(*_)

    _register(self, required, provided, name, _factory)
    return


zope.interface.adapter.BaseAdapterRegistry.register = register
_fromUnicode = zope.configuration.fields.GlobalObject.fromUnicode

def fromUnicode(self, u):
    """This method wraps ``fromUnicode`` so strings that begin with a
    dash are wrapped as a discriminator."""
    if u.startswith('-'):
        return discriminator(self.fromUnicode(u[1:]))
    return _fromUnicode(self, u)


zope.configuration.fields.GlobalObject.fromUnicode = fromUnicode