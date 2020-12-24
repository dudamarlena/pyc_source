# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\sake\xreload.py
# Compiled at: 2011-02-21 01:24:11
"""Alternative to reload().

This works by executing the module in a scratch namespace, and then
patching classes, methods and functions in place.  This avoids the
need to patch instances.  New objects are copied into the target
namespace.

Some of the many limitiations include:

- Global mutable objects other than classes are simply replaced, not patched

- Code using metaclasses is not handled correctly

- Code creating global singletons is not handled correctly

- Functions and methods using decorators (other than classmethod and
  staticmethod) is not handled correctly

- Renamings are not handled correctly

- Dependent modules are not reloaded

- When a dependent module contains 'from foo import bar', and
  reloading foo deletes foo.bar, the dependent module continues to use
  the old foo.bar object rather than failing

- Frozen modules and modules loaded from zip files aren't handled
  correctly

- Classes involving __slots__ are not handled correctly
"""
import gc, imp, logging, marshal, sys, types

def xreload(mod):
    """Reload a module in place, updating classes, methods and functions.

    Args:
      mod: a module object

    Returns:
      The (updated) input object itself.
    """
    modname = mod.__name__
    modns = mod.__dict__
    i = modname.rfind('.')
    if i >= 0:
        pkgname, modname = modname[:i], modname[i + 1:]
    else:
        pkgname = None
    if pkgname:
        pkg = sys.modules[pkgname]
        path = pkg.__path__
    else:
        pkg = None
        path = None
    stream, filename, (suffix, mode, kind) = imp.find_module(modname, path)
    try:
        if kind not in (imp.PY_COMPILED, imp.PY_SOURCE):
            return reload(mod)
        if kind == imp.PY_SOURCE:
            source = stream.read() + '\n'
            code = compile(source, filename, 'exec')
        else:
            code = marshal.load(stream)
    finally:
        if stream:
            stream.close()

    tmpns = modns.copy()
    modns.clear()
    modns['__name__'] = tmpns['__name__']
    modns['__file__'] = tmpns['__file__']
    exec (
     code, modns)
    oldnames = set(tmpns)
    newnames = set(modns)
    for name in oldnames & newnames:
        modns[name] = _update(tmpns[name], modns[name])

    return mod


def _update(oldobj, newobj):
    """Update oldobj, if possible in place, with newobj.

    If oldobj is immutable, this simply returns newobj.

    Args:
      oldobj: the object to be updated
      newobj: the object used as the source for the update

    Returns:
      either oldobj, updated in place, or newobj.
    """
    if oldobj is newobj:
        return newobj
    if type(oldobj) is not type(newobj):
        return newobj
    if hasattr(newobj, '__reload_update__'):
        return newobj.__reload_update__(oldobj)
    if isinstance(newobj, types.ClassType):
        return _update_class(oldobj, newobj)
    if isinstance(newobj, types.TypeType):
        return _update_class(oldobj, newobj)
    if isinstance(newobj, types.FunctionType):
        return _update_function(oldobj, newobj)
    if isinstance(newobj, types.MethodType):
        return _update_method(oldobj, newobj)
    if isinstance(newobj, classmethod):
        return _update_classmethod(oldobj, newobj)
    if isinstance(newobj, staticmethod):
        return _update_staticmethod(oldobj, newobj)
    return newobj


def _update_function(oldfunc, newfunc):
    """Update a function object."""
    oldfunc.__doc__ = newfunc.__doc__
    oldfunc.__dict__.update(newfunc.__dict__)
    oldfunc.func_code = newfunc.func_code
    return oldfunc


def _update_method(oldmeth, newmeth):
    """Update a method object."""
    _update(oldmeth.im_func, newmeth.im_func)
    return oldmeth


def _update_class(oldclass, newclass):
    """Update a class object."""
    olddict = oldclass.__dict__
    newdict = newclass.__dict__
    oldnames = set(olddict)
    newnames = set(newdict)
    for name in newnames - oldnames:
        setattr(oldclass, name, newdict[name])

    for name in oldnames - newnames:
        delattr(oldclass, name)

    for name in oldnames & newnames - set(['__dict__', '__doc__']):
        try:
            setattr(oldclass, name, _update(olddict[name], newdict[name]))
        except AttributeError:
            logging.root.exception('Ignoring exception')

    UpdateGlobalReferences(newclass, oldclass)
    return oldclass


def _update_classmethod(oldcm, newcm):
    """Update a classmethod update."""
    _update(oldcm.__get__(0), newcm.__get__(0))
    return newcm


def _update_staticmethod(oldsm, newsm):
    """Update a staticmethod update."""
    _update(oldsm.__get__(0), newsm.__get__(0))
    return newsm


def UpdateGlobalReferences(oldBaseClass, newBaseClass):
    for ob1 in gc.get_referrers(oldBaseClass):
        if type(ob1) is dict:
            for k, v in ob1.items():
                if v is oldBaseClass:
                    logging.root.info("Setting '%s' to '%s' in '%s'", k, newBaseClass, ob1.get('__file__'))
                    ob1[k] = newBaseClass