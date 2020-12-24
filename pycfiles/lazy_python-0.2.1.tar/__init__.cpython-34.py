# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/yui/projects/python/lazy_python/lazy/include/__init__.py
# Compiled at: 2015-10-15 01:38:34
# Size of source mod 2**32: 222 bytes
from os.path import dirname

def get_include():
    """Return the include directory for lazy.

    Returns
    -------
    include_dir : str
        The path to the include directory.
    """
    return dirname(__file__)