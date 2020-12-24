# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_core/field/enum.py
# Compiled at: 2009-09-07 17:44:28


def Enum(field, enum, key_func=None):
    """
    Enum is an adapter to another field: it will just change its display
    attribute. It uses a dictionnary to associate a value to another.

    key_func is an optional function with prototype "def func(key)->key"
    which is called to transform key.
    """
    display = field.createDisplay
    if key_func:

        def createDisplay():
            try:
                key = key_func(field.value)
                return enum[key]
            except LookupError:
                return display()

    else:

        def createDisplay():
            try:
                return enum[field.value]
            except LookupError:
                return display()

    field.createDisplay = createDisplay
    field.getEnum = lambda : enum
    return field