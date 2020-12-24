# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treelib/misc.py
# Compiled at: 2020-02-27 08:49:21
# Size of source mod 2**32: 1575 bytes
import functools
from warnings import warn, simplefilter

def deprecated(alias):

    def real_deco(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            simplefilter('always', DeprecationWarning)
            warn(('Call to deprecated function "{}"; use "{}" instead.'.format(func.__name__, alias)), category=DeprecationWarning,
              stacklevel=2)
            simplefilter('default', DeprecationWarning)
            return func(*args, **kwargs)

        return wrapper

    return real_deco