# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/apryor/projects/flaskerize/flaskerize/utils.py
# Compiled at: 2019-09-08 08:53:32
# Size of source mod 2**32: 1129 bytes
from typing import List, Tuple

def split_file_factory(path: str, delim: str=':', default_func_name: str='create_app') -> Tuple[(str, str)]:
    """Split the gunicorn-style module:factory syntax for the provided app factory"""
    import os
    if delim in path:
        _split = path.split(delim)
        if len(_split) != 2:
            raise ValueError('Failure to parse path to app factory. Syntax should be filename:function_name')
        filename, func = _split
    else:
        filename = path
        func = default_func_name
    if os.path.isdir(filename):
        if os.path.isfile(filename + '/__init__.py'):
            filename += '/__init__.py'
        else:
            raise SyntaxError(f"Unable to parse factory input. Input file '{filename}' is a directory, but not a package.")
    if not os.path.exists(filename):
        if os.path.exists(filename + '.py'):
            filename = filename + '.py'
    return (
     filename, func)