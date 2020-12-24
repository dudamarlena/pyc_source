# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/package/canonical.py
# Compiled at: 2019-01-22 13:34:55
# Size of source mod 2**32: 655 bytes
from functools import partial
from inspect import getmodule, getmembers, isclass, isroutine
from typeguard import check_argument_types
from typing import Callable

def name(obj) -> str:
    """This helper function attempts to resolve the dot-colon import path for a given object.
        
        Specifically searches for classes and methods, it should be able to find nearly anything at either the module
        level or nested one level deep.  Uses ``__qualname__`` if available.
        """
    if not isroutine(obj):
        if not hasattr(obj, '__name__'):
            if hasattr(obj, '__class__'):
                obj = obj.__class__
    module = getmodule(obj)
    return module.__name__ + ':' + obj.__qualname__