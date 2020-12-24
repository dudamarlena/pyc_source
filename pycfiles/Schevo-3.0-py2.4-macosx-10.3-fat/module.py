# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/schevo/lib/module.py
# Compiled at: 2007-03-21 14:34:41
"""Module remembering/forgetting.

For copyright, license, and warranty, see bottom of file.
"""
import imp, sys
try:
    from py.code import compile
except ImportError:
    pass

MODULES = []

def forget(module):
    """Remove module from sys.modules"""
    name = module.__name__
    if name in sys.modules:
        del sys.modules[name]
    if name in MODULES:
        MODULES.remove(module)


def from_string(source, name=''):
    """Return a named Python module containing source."""
    source = source.strip() + '\n'
    module = imp.new_module(name)
    code = compile(source, name, 'exec')
    exec code in module.__dict__
    return module


def remember(module, complain=True):
    """Add a module to sys.modules.

    If module has a callable called _remember_hook(), it will call it,
    passing this function as an argument.  This hook can be used to
    remember dependencies.
    """
    name = module.__name__
    if name in sys.modules.keys() and complain:
        raise ValueError, 'module conflicts with an existing one'
    sys.modules[name] = module
    MODULES.append(module)