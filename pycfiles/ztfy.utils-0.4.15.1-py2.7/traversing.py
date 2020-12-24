# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/utils/traversing.py
# Compiled at: 2014-10-07 05:33:01
from zope.interface import Interface

def getParent(context, interface=Interface, allow_context=True):
    """Get first parent of the given context that implements given interface"""
    if allow_context:
        parent = context
    else:
        parent = getattr(context, '__parent__', None)
    while parent is not None:
        if interface.providedBy(parent):
            return interface(parent)
        parent = getattr(parent, '__parent__', None)

    return


def resolve(name, module=None):
    name = name.split('.')
    if not name[0]:
        if module is None:
            raise ValueError('relative name without base module')
        module = module.split('.')
        name.pop(0)
        while not name[0]:
            module.pop()
            name.pop(0)

        name = module + name
    used = name.pop(0)
    found = __import__(used)
    for n in name:
        used += '.' + n
        try:
            found = getattr(found, n)
        except AttributeError:
            __import__(used)
            found = getattr(found, n)

    return found