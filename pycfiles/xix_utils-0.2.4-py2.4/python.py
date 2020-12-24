# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xix/utils/python.py
# Compiled at: 2007-01-21 20:27:15
"""
python.py

Python-specific utilities for python modules.

Copyright (c) 2005 Drew Smathers
See LICENSE for details.

"""
__author__ = 'Drew Smathers'
__copyright__ = '(c) 2005 Drew Smathers'
__version__ = '$Revision: 399 $'[11:-2]
__license__ = 'MIT'
import os, inspect
from interfaces import IModuleWrapper
from comp.interface import implements
import inspect, warnings, sys
pj = os.path.join

def setAll(all, locals, *exclude):
    """
    Convenience method for use at end of module to set components
    of modules.
    
    @param all: __all__
    @type  all: list
    @param locals: keys in locals of calling module
    @type  locals: list
    @param exclude: names to excude
    @type  exclude: string
    @deprecated use allexcept instead
    """
    for local in locals:
        if local not in exclude and local[0] != '_':
            all.append(local)

    return all


def _setAll(all, locals, *exclude):
    for local in locals:
        if local not in exclude and local[0] != '_':
            all.append(local)

    return all


def getCallersGlobals(internal_ns=None):
    """
    Get globals of caller.

    @param internal_ns: names to ignore in stack search
    @return globals dictionary of caller
    """
    intns = internal_ns or []
    intns = list(intns)
    if __name__ not in intns:
        intns.append(__name__)
    callers_frame = None
    try:
        callers_frame = inspect.stack()[1][0]
        loop_counter = 2
        while callers_frame.f_globals['__name__'] in intns:
            del callers_frame
            callers_frame = inspect.stack()[loop_counter][0]
            loop_counter += 1
            if loop_counter == 128:
                break

        globs = callers_frame.f_globals
        return globs
    finally:
        try:
            del callers_frame
        except UnboundLocalError:
            pass

    return


def getCallersLocals(internal_ns=None):
    """
    Get locals of caller.

    @param internal_ns: names to ignore in stack search
    @return locals dictionary of caller
    """
    intns = internal_ns or []
    intns = list(intns)
    if __name__ not in intns:
        intns.append(__name__)
    callers_frame = None
    try:
        callers_frame = inspect.stack()[1][0]
        loop_counter = 2
        while callers_frame.f_globals['__name__'] in intns:
            del callers_frame
            callers_frame = inspect.stack()[loop_counter][0]
            loop_counter += 1
            if loop_counter == 128:
                break

        locs = callers_frame.f_locals
        return locs
    finally:
        del callers_frame
    return


def _getCallerLocals():
    callers_frame = None
    try:
        callers_frame = inspect.stack()[1][0]
        loop_counter = 2
        while callers_frame.f_globals['__name__'] == __name__:
            del callers_frame
            callers_frame = inspect.stack()[loop_counter][0]
            loop_counter += 1
            if loop_counter == 128:
                break

        return callers_frame.f_locals
    finally:
        del callers_frame
    return


def allexcept(*exclude):
    """Return __all__ list containing everything in locals of callers except
    names indicated in exclude.
    
    Note: __all__ list defined for a module indicate what will be imported by:

    <pre>
    from mymodule import *
    </pre>

    @param exclude: names to exclude in __all__
    """
    warnings.warn('allexcept will be deprecated in future version of xix.utils')
    return _setAll([], _getCallerLocals(), *exclude)


def fileHere(filename):
    """Get absolute path of filename in same directory as source file
    of calling module.

    @param filename: relative path of file
    @return absolute path of file
    """
    warnings.warn('fileHere is deprecated')
    src_file = getCallersGlobals([__name__])['__file__']
    return src_file[:-len(src_file.split(os.path.sep)[-1:][0])] + filename


def isValidName(name):
    """Return True if name is valid name in Python, False otherwise.

    @param name: name to test
    @type  name: string
    """

    class _:
        __module__ = __name__

    try:
        _ = _()
        ns = dict(_=_)
        exec (
         '_.%s = 1' % name, ns, ns)
    except SyntaxError:
        return False

    return True


def buildPackagePath(root, nodes):
    """Build a python package path nondestructively. Intermittent  __init__.py
    modules are also created along the way as needed.

    @todo: unit testing, write _build_py_tree

    @param root: absolute path of package root
    @type  root: string
    @param node: list of directory names
    @param node: list
    @rais NotImplementError: when called
    """
    raise NotImplementedError, 'buildPackagePath is not implemented'
    if not nodes:
        return ''
    nodes_cpy = list(nodes)
    next = nodes_cpy.pop(0)
    newroot = pj(root, next)
    if not os.path.exists(newroot):
        os.mkdir(newroot)
    initf = pj(newroot, '__init__.py')
    if not os.path.exists(initf):
        fp = open(initf, 'w')
        fp.close()


def argorattr(obj, *names_defaults):
    """Return mixed default values or values from attribute
    of object, if object has the attribute by the name.

    Example Usage:

    >>> class Foo:
    ...     a = 1
    ...     b = 2
    ...
    >>> f = Foo()
    >>> a, b, c = argorattr(f, ('a',-1), ('b',-2), ('c',-3))
    >>> print a, b, c
    1 2 -3

    @param names_defaults: (name, default_value) tuples
    """
    ret = ()
    for (name, default) in names_defaults:
        if hasattr(obj, name):
            ret += (getattr(obj, name),)
        else:
            ret += (default,)

    return ret


class _ArgContainer:
    __module__ = __name__
    DUP_ARG = 'duplicate keyword argument'

    def __init__(self, func):
        self.argspec = inspect.getargspec(func)
        if self.argspec[3]:
            self.karg_names = self.argspec[0][-len(self.argspec[3]):]
        else:
            self.karg_names = []
        self.karg_values = self.argspec[3] or []
        self.consumed_karg_names = {}
        self.argct = len(self.argspec[0]) - len(self.karg_names)
        self.kargct = len(self.karg_names)
        self.got_pargs = []
        self.got_kargs = {}

    def update(self, *args, **kargs):
        tokargs = []
        topargs = args
        delta = 0
        if not self.argspec[1] and len(args) + len(self.got_pargs) > self.argct:
            if self.argct != len(self.got_pargs):
                delta = self.argct - len(self.got_pargs)
                tokargs = args[delta:]
                topargs = args[:delta]
            else:
                tokargs = args
        for arg in tokargs:
            try:
                key = self.karg_names.pop(0)
                self.consumed_karg_names[key] = True
                self.got_kargs[key] = arg
            except IndexError:
                self.got_pargs.append(arg)

        for arg in topargs:
            self.got_pargs.append(arg)

        for (key, value) in kargs.items():
            self.got_kargs[key] = value
            self.consumed_karg_names[key] = True

        if len(self.got_pargs) >= self.argct:
            for (key, value) in zip(self.karg_names, self.karg_values):
                if not self.consumed_karg_names.has_key(key):
                    self.got_kargs[key] = value

            return True


class Curried:
    """WARNING: implementation is broken.
    
    Example Usage:

    >>> def three(a, b, c=4):
    ...     return a, b, c
    ...
    >>> curried = Curried(three, 2, 3)
    
    #>>> print curried()
    #(2, 3, 4)
    
    """
    __module__ = __name__

    def __init__(self, func, *pargs, **kwargs):
        import warnings
        warnings.warn('Curried is broken!  Do not use this class (yet).')
        self.func = func
        self.argContainer = _ArgContainer(func)
        self._call(pargs, kwargs, defer=True)

    def __call__(self, *pargs, **kwargs):
        return self._call(pargs, kwargs, defer=False)

    def _call(self, pargs, kwargs, defer=False):
        cont = self.argContainer
        result = cont.update(*pargs, **kwargs)
        if result and not defer:
            args, kargs = cont.got_pargs, cont.got_kargs
            r = self.func(*args, **kargs)
        return self


class CurriedCallable:
    """CurriedCallable is like curried but must be called with
    required remaining args => only one call after initialization.
    
    Example Usage:

    >>> def addThree(a, b, c=4):
    ...     return a + b + c
    ...
    >>> curried = CurriedCallable(addThree, 2, 3)
    >>> print curried()
    9
    >>> curried = CurriedCallable(addThree, 2, 3, c=5)
    >>> print curried()
    10

    Supplying an additional argument to curried:

    >>> curried = CurriedCallable(addThree, 2, 3)
    >>> print curried(c=20)
    25
    
    """
    __module__ = __name__

    def __init__(self, func, *pargs, **kwargs):
        import warnings
        warnings.warn('CurriedCallable is broken!  Do not use this class (yet).')
        self.func = func
        self.pargs = list(pargs)
        self.kwargs = dict(kwargs)

    def __call__(self, *pargs, **kwargs):
        kws = dict(self.kwargs)
        kws.update(dict(kwargs))
        args = self.pargs + list(pargs)
        return self.func(*args, **kws)