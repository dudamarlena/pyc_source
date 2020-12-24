# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tracbmacros/util.py
# Compiled at: 2010-07-17 20:03:31
"""Helper classes and functions

Copyright 2009-2011 Olemis Lang <olemis at gmail.com>
Licensed under the Apache License
"""
__author__ = 'Olemis Lang'
from trac.core import TracError, Interface
from pkg_resources import EntryPoint

def load_object(objpath):
    """Dynamically load an object at a given global object path
    following `pkg_resources` syntax.
    """
    ep = EntryPoint.parse('x=' + objpath)
    return ep.load(require=False)


def load_interface(objpath):
    """Dynamically load a Trac interface. Raise `TracError` if path 
    leads to an invalid object.
    """
    intf = load_object(objpath)
    if not isinstance(intf, Interface):
        raise TracError('Trac interface expected at `%s`' % (objpath,), 'Invalid object')
    else:
        return intf