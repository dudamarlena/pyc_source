# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/attrcheck/__init__.py
# Compiled at: 2011-10-10 02:08:15
"""
    attrcheck: attribution checker

    This module provides a simple attribution checker implemented as a decorator.
    All functionality are provided as keyword arguments of the decorator.

    Sample example of usage is following:

        >>> from attrcheck import attrcheck
        >>> @attrcheck(x=['real'], y=['index', 'strip'], z=dir(list))
        ... def foo(x, y, z=[]): pass

    The code above means the following:

        >>> def foo(x, y, z=[]):
        ...     if not hasattr(x, 'real'):
        ...         raise AttributeError
        ...     if not hasattr(y, 'index'):
        ...         raise AttributeError
        ...     if not hasattr(y, 'strip'):
        ...         raise AttributeError
        ...     for name in dir(list):
        ...         if not hasattr(z, name):
        ...             raise AttributeError

    In addition, attrcheck can check default argument values.
    Thus, the following code throws AttributeError.

        >>> @attrcheck(y=dir(str))
        ... def bar(x, y=[]): pass
"""
__author__ = 'Jun Namikawa'
__email__ = 'jnamika@gmail.com'
__version__ = '0.1.2'
__license__ = 'ISC License (ISCL)'
from attrcheck import attrcheck