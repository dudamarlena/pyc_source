# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/typecheck/doctest_support.py
# Compiled at: 2006-05-27 18:37:17
"""
This module allows doctest to find typechecked functions.

Currently, doctest verifies functions to make sure that their
globals() dict is the __dict__ of their module. In the case of
decorated functions, the globals() dict *is* not the right one.

To enable support for doctest do:
    
    import typecheck.doctest_support

This import must occur before any calls to doctest methods.
"""

def __DocTestFinder_from_module(self, module, object):
    """
    Return true if the given object is defined in the given
    module.
    """
    import inspect
    if module is None:
        return True
    elif inspect.isfunction(object) or inspect.isclass(object):
        return module.__name__ == object.__module__
    elif inspect.getmodule(object) is not None:
        return module is inspect.getmodule(object)
    elif hasattr(object, '__module__'):
        return module.__name__ == object.__module__
    elif isinstance(object, property):
        return True
    else:
        raise ValueError('object must be a class or function')
    return


import doctest as __doctest
__doctest.DocTestFinder._from_module = __DocTestFinder_from_module