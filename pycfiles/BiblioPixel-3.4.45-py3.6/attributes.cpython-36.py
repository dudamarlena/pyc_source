# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/project/attributes.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 385 bytes


def check(kwds, name):
    if kwds:
        msg = ', '.join('"%s"' % s for s in sorted(kwds))
        s = '' if len(kwds) == 1 else 's'
        raise ValueError('Unknown attribute%s for %s: %s' % (s, name, msg))


def set_reserved(value, section, name=None, data=None, **kwds):
    check(kwds, '%s %s' % (section, value.__class__.__name__))
    value.name = name
    value.data = data