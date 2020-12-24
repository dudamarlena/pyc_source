# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/schevopolicy/convert.py
# Compiled at: 2008-01-19 12:32:25
"""Conversion functions between restricted and non-restricted objects.

For copyright, license, and warranty, see bottom of file.
"""
import sys
from schevo.lib import optimize
from schevopolicy.rentity import RestrictedEntity

def unrestricted_args(args, kw):
    """Return a tuple of (arguments, keyword arguments) based on the
    given arguments and keyword arguments, where RestrictedEntity
    instances have been converted to regular entity instances.

    XXX: Does not handle EntityList, EntitySet, or EntitySetSet
    values.
    """
    newargs = []
    newkw = {}
    for arg in args:
        if isinstance(arg, RestrictedEntity):
            arg = arg._entity
        newargs.append(arg)

    for (key, value) in kw.iteritems():
        if isinstance(value, RestrictedEntity):
            value = value._entity
        newkw[key] = value

    return (
     newargs, newkw)


optimize.bind_all(sys.modules[__name__])