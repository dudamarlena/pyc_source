# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\dragonfly\actions\action_function.py
# Compiled at: 2009-04-01 11:30:07
"""
Function action
============================================================================

The :class:`Function` action wraps a callable, optionally with some 
default keyword argument values.  On execution, the execution data 
(commonly containing the recognition extras) are combined with the 
default argument values (if present) to form the arguments with which 
the callable will be called.

Simple usage::

    >>> def func(count):
    ...     print "count:", count
    ...
    >>> action = Function(func)
    >>> action.execute({"count": 2})
    count: 2
    >>> action.execute({"count": 2, "flavor": "vanilla"})
    count: 2          # Additional keyword arguments are ignored.

Usage with default arguments::

    >>> def func(count, flavor):
    ...     print "count:", count
    ...     print "flavor:", flavor
    ...
    >>> action = Function(func, flavor="spearmint")
    >>> action.execute({"count": 2})
    count: 2
    flavor: spearmint
    >>> action.execute({"count": 2, "flavor": "vanilla"})
    count: 2
    flavor: vanilla

Class reference
----------------------------------------------------------------------------

"""
from inspect import getargspec
from .action_base import ActionBase, ActionError

class Function(ActionBase):
    """ Call a function with extra keyword arguments. """

    def __init__(self, function, **defaults):
        """
            Constructor arguments:
             - *function* (callable) --
               the function to call when this action is executed
             - defaults --
               default keyword-values for the arguments with which
               the function will be called

        """
        ActionBase.__init__(self)
        self._function = function
        self._defaults = defaults
        self._str = function.__name__
        (args, varargs, varkw, defaults) = getargspec(self._function)
        if varkw:
            self._filter_keywords = False
        else:
            self._filter_keywords = True
        self._valid_keywords = set(args)

    def _execute(self, data=None):
        arguments = dict(self._defaults)
        if isinstance(data, dict):
            arguments.update(data)
        if self._filter_keywords:
            invalid_keywords = set(arguments.keys()) - self._valid_keywords
            for key in invalid_keywords:
                del arguments[key]

        try:
            self._function(**arguments)
        except Exception, e:
            self._log.exception('Exception from function %s:' % self._function.__name__)
            raise ActionError('%s: %s' % (self, e))