# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/resolve/__init__.py
# Compiled at: 2008-11-24 11:46:12


def resolve(dotted):
    names = dotted.split('.')
    l_names = len(names)
    current = names[0]
    i = 0
    for name in names:
        i += 1
        try:
            o = __import__(current)
        except ImportError:
            if i == l_names:
                raise
        else:
            break

    for name in names[i:]:
        o = getattr(o, name)

    return o