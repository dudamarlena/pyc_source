# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.11.1-i386/egg/z3c/discriminator/discriminator.py
# Compiled at: 2007-11-26 11:24:36


def discriminator(iface):
    """This method creates an interface class derived from ``iface`` that behaves
    and identifies exactly like ``iface`` except it is marked as a discriminator
    by providing ``__discriminated__``."""

    class meta(type(iface)):
        __module__ = __name__

        def __init__(self, name, bases=(), attrs=None, **kwargs):
            del attrs['__metaclass__']
            super(meta, self).__init__(name, bases=bases, attrs=attrs, **kwargs)

        def __eq__(self, other):
            if other is iface or other is self:
                return True

        def __hash__(self):
            return hash(iface)

    class _(iface):
        __module__ = __name__
        __metaclass__ = meta

    _.__discriminated__ = iface
    return _