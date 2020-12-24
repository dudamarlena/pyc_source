# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/watchm8/lib.py
# Compiled at: 2017-09-11 04:54:27


def class_loader(name):
    """
    Imports and returns given class/func/variable/module name

    Args:
        name: A string of what to import ex. foo.bar.MyClass

    Returns:
        class/func/variable/module
    """
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)

    return mod