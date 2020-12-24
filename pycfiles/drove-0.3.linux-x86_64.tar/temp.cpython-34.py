# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/drove/lib/python3.4/site-packages/drove/util/temp.py
# Compiled at: 2015-01-20 05:42:58
# Size of source mod 2**32: 1483 bytes
"""This module provides utilities related with temporary files
and directories which are auto-removed
"""
import sys, shutil, tempfile, contextlib

@contextlib.contextmanager
def directory():
    """Create temporary directory and destroy it after use

    >>> with directory() as d:
    ...    # do stuff
    """
    temp_dir = tempfile.mkdtemp()
    try:
        yield temp_dir
    finally:
        shutil.rmtree(temp_dir)


@contextlib.contextmanager
def variables(vars):
    """Do something with some variable alterated

    >>> with variables({"sys.args": []}):
    ...     # do stuff
    """

    def _get_set_vals(childs, ctx, value):
        if len(childs) == 1:
            ret = getattr(ctx, childs[0])
            setattr(ctx, childs[0], value)
            return ret
        else:
            return _get_set_vals(childs[1:], getattr(ctx, childs[0]), value)

    def _get_set_orig_keys(vars):
        old = {}
        for key, value in vars.items():
            if '.' not in key:
                raise ValueError('To set temporary variable ' + 'must be into a module')
            mod = key.split('.')
            ctx = sys.modules[mod[0]]
            old[key] = _get_set_vals(mod[1:], ctx, value)

        return old

    old = _get_set_orig_keys(vars)
    try:
        yield
    finally:
        _get_set_orig_keys(old)