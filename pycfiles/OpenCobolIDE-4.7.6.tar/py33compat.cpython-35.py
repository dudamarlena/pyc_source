# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-4yaip7h6/keyring/keyring/py33compat.py
# Compiled at: 2016-12-29 05:40:26
# Size of source mod 2**32: 660 bytes
"""
Compatibility support for Python 3.3. Remove when Python 3.3 support is
no longer required.
"""
from .py27compat import builtins

def max(*args, **kwargs):
    """
    Add support for 'default' kwarg.

    >>> max([], default='res')
    'res'

    >>> max(default='res')
    Traceback (most recent call last):
    ...
    TypeError: ...

    >>> max('a', 'b', default='other')
    'b'
    """
    missing = object()
    default = kwargs.pop('default', missing)
    try:
        return builtins.max(*args, **kwargs)
    except ValueError as exc:
        if 'empty sequence' in str(exc) and default is not missing:
            return default
        raise