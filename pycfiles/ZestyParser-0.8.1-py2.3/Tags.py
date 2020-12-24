# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.9.1-i386/egg/ZestyParser/Tags.py
# Compiled at: 2007-04-30 17:11:22
"""
@version: 0.8.1
@author: Adam Atlas
@copyright: Copyright 2006-2007 Adam Atlas. Released under the MIT license (see LICENSE.txt).
@contact: adam@atlas.st

Tags is a utility module providing an easy way to label objects in abstract parse trees without defining a class for each one. It supersedes the L{AHT} module.

This module provides a global "Tags" object; you create a tag by accessing any attribute on it. A tag is a callable object, suitable for use as an L{AbstractToken} C{to} parameter, or, if it is more convenient (e.g. when you must use C{>>}), a callback. Later, you can check if a given tag has been applied to an object by checking for membership with C{in}. For example::

    >>> l = [1, 2, 3]
    >>> l in Tags.thing
    False
    >>> Tags.thing(l)
    [1, 2, 3]
    >>> l in Tags.thing
    True
"""
__all__ = (
 'Tags',)

class _Env(object):
    """
    @see: L{Tags}
    """
    __module__ = __name__
    _tagobjs = {}

    def __getattr__(self, attr):
        if attr not in self._tagobjs:
            self._tagobjs[attr] = _Tag(attr)
        return self._tagobjs[attr]


Tags = _Env()

class _Tag(object):
    __module__ = __name__

    def __init__(self, name):
        self.name = name
        self.objects = []

    def __call__(self, arg):
        self.objects.append(arg)
        return arg

    def __contains__(self, arg):
        return arg in self.objects

    def __repr__(self):
        return '<Tag %s>' % self.name