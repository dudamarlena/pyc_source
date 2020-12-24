# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.9.1-i386/egg/ZestyParser/AHT.py
# Compiled at: 2007-04-30 17:11:11
"""
@version: 0.8.1
@author: Adam Atlas
@copyright: Copyright 2006-2007 Adam Atlas. Released under the MIT license (see LICENSE.txt).
@contact: adam@atlas.st

This module is now deprecated in favour of L{Tags}. The documentation and classes are still available to assist in converting code that uses AHT, but this module may be removed in a future version. In general, given some AHT environment E, code can be converted to use Tags by changing C{callback=/to=/as=/>> E.x} to C{callback=/to=/>> Tags.x} and C{isinstance(y, E.x)} to C{y in Tags.x}.

AHT (Ad Hoc Types) is a utility module providing an easy way to generate "labels" for objects in abstract parse trees without defining a class for each one.

To use it, create an instance of L{Env}. Now you can access any property on it and get a unique type for that name. The first time such a type is called, it becomes a subclass of the type of whatever it is passed. For example, C{EnvInstance.SomeEntity("hi")} marks C{SomeEntity} as being a subclass of C{str}, and returns an instance of itself initialized with C{"hi"}.) Now you can check at any time with nothing more than a C{isinstance(something, EnvInstance.SomeEntity)} how a piece of data was instantiated.

Ad Hoc Types are primarily intended to be used in conjunction with L{AbstractToken} types, where you should set it as the C{as} parameter, or, if it is more convenient (e.g. when you must use C{>>}), as its callback.
"""
__all__ = (
 'Env',)

class Env:
    """
    @see: L{AHT}
    """
    __module__ = __name__
    _aht_types = {}

    def __getattr__(self, attr):
        if attr in self._aht_types:
            return self._aht_types[attr]
        else:
            return _AHTFactory(self, attr)


class _AHTFactory:
    __module__ = __name__

    def __init__(self, env, name):
        (self.env, self.name) = (env, name)

    def __call__(self, arg):
        if self.name not in self.env._aht_types:
            self.env._aht_types[self.name] = type(self.name, (arg.__class__,), {})
        return self.env._aht_types[self.name](arg)