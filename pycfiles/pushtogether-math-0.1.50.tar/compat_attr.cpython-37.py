# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/rmcgover/src/pushsource/src/pushsource/_impl/compat_attr.py
# Compiled at: 2020-01-30 19:06:48
# Size of source mod 2**32: 299 bytes
import sys, attr

def s():
    kwargs = {'frozen': True}
    if sys.version_info >= (3, ):
        kwargs['kw_only'] = True
    return (attr.s)(**kwargs)


ib = attr.ib
evolve = attr.evolve
Factory = attr.Factory