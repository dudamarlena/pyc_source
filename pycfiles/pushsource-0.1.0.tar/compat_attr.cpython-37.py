# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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