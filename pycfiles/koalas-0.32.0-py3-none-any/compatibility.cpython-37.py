# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/databricks/koalas/dask/compatibility.py
# Compiled at: 2019-04-23 07:44:26
# Size of source mod 2**32: 261 bytes
import inspect
string_types = (str,)

def get_named_args(func):
    """Get all non ``*args/**kwargs`` arguments for a function"""
    s = inspect.signature(func)
    return [n for n, p in s.parameters.items() if p.kind == p.POSITIONAL_OR_KEYWORD]