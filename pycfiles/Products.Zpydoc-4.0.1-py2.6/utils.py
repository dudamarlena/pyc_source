# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/Zpydoc/utils.py
# Compiled at: 2011-09-28 02:31:46
"""$id$"""
import string, os, pydoc, sys, inspect, types, __builtin__
all_paths = pydoc.pathdirs
pythonpath = all_paths()
zopepath = [
 os.path.join(os.environ.get('SOFTWARE_HOME'), 'Products'),
 os.path.join(os.environ.get('INSTANCE_HOME'), 'Products')]
sane_pythonpath = [
 'builtin__'] + pythonpath + zopepath
sane_pythonpath.sort()
all_modules = map(lambda x: x.__name__, filter(lambda x: hasattr(x, '__path__'), sys.modules.values()))
all_modules.sort()

def pydoc_encode(name):
    if name[0] == '_':
        return '-%s' % name[1:]
    return name


def pydoc_decode(name):
    if name[0] == '-':
        return '_%s' % name[1:]
    return name


def implementsMethod(object):
    try:
        return isinstance(object, types.MethodType) or hasattr(object, '__doc__') and hasattr(object, '__name__') and hasattr(object, 'im_class') and hasattr(object, 'im_func') and hasattr(object, 'im_self') and inspect.isfunction(object.im_func)
    except:
        raise


def locate(path, forceload=0):
    """
    find and wrecklessly import a module a module if we don't already have it!!
    """
    parts = [ part for part in string.split(path, '.') if part ]
    (module, n) = (None, 0)
    while n < len(parts):
        nextmodule = pydoc.safeimport(string.join(parts[:n + 1], '.'), forceload)
        if nextmodule:
            module, n = nextmodule, n + 1
        else:
            break

    if module:
        object = module
        for part in parts[n:]:
            try:
                object = getattr(object, part)
            except AttributeError:
                return

        return object
    else:
        if hasattr(__builtin__, path):
            return getattr(__builtin__, path)
        return