# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/pyasn1/pyasn1/compat/calling.py
# Compiled at: 2018-07-11 18:15:32
from sys import version_info
__all__ = [
 'callable']
if (2, 7) < version_info[:2] < (3, 2):
    import collections

    def callable(x):
        return isinstance(x, collections.Callable)


else:
    callable = callable