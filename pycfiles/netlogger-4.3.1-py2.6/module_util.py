# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/module_util.py
# Compiled at: 2010-08-06 23:47:37
"""
Utility functions/classes for dynamic module and class loading
"""
__rcsid__ = '$Id: module_util.py 25065 2010-08-07 03:47:36Z dang $'
__author__ = 'Dan Gunter'
import imp, os, sys
from netlogger import class_info
from netlogger import util

class ModuleLoadError(Exception):
    """Use this exception for reporting errors in loadModule().
    """

    def pathStr(self, path):
        return (':').join(path)


class ModuleNotFound(ModuleLoadError):

    def __init__(self, module, path, err):
        msg = "No module '%s' in path '%s': %s" % (
         module, self.pathStr(path), err)
        ModuleLoadError.__init__(self, msg)


class ModuleImportError(ModuleLoadError):

    def __init__(self, module, path, err, tb):
        msg = "Error importing module '%s' in path '%s': %s" % (
         module, self.pathStr(path), err)
        msg = msg + tb
        ModuleLoadError.__init__(self, msg)


def list_modules(*subdirs):
    """Get a list of available modules under 
    netlogger.<subdir1>.<subdir2>.<{etc.}>

    For example: list_modules('parsers','modules')

    Raises ModuleImportError if the parent module can't be found.
    """
    try:
        minfo = imp.find_module('netlogger', sys.path)
    except ImportError, E:
        raise ModuleImportError("Could not find package 'netlogger'")

    filename = minfo[1]
    path = os.path.join(filename, *subdirs)
    if not os.path.isdir(path):
        raise ModuleImportError("Could not find path '%s'" % path)
    mlist = [ f[:-3] for f in os.listdir(path) if f.endswith('.py') if not f.startswith('_') ]
    mlist.sort()
    return mlist


def module_info(module_type, module_name, clazz, wraplen=65):
    """Build a string describing the purpose and options of a
    given module.
    
    The docstring for the 'clazz' object is used as the source
    of the description and parameters.
    """
    info = class_info.Info(clazz)
    desc = info.get_desc()
    if desc:
        desc = util.wrap(desc, wraplen, leader='                ')
    else:
        desc = '(None)'
    s = '* %s name:  %s\n* Description:  %s\n* Parameters:' % (
     module_type.title(), module_name, desc)
    params = info.get_parameters()
    if params:
        s += '\n\n'
        maxlen = max([ len(p.name) for p in params ])
        leader = ' ' * (maxlen + 6)
        for p in params:
            pstr = '    %-*s%s' % (maxlen + 2, p.name, p.desc)
            if not p.desc.endswith('.'):
                pstr += '.'
            if p.values:
                pstr += ' values=(%s)' % (',').join(p.values)
            if p.default_value:
                pstr += ' [%s]' % p.default_value
            pstr = util.wrap(pstr, wraplen, leader=leader)
            s += pstr + '\n\n'

    else:
        s += '  (None)\n'
    return s


def load_module(module_name, pre_path=None, sys_path=True, post_path=None):
    """Find and load a module in piece-by-piece.

    Raise: 

      - subclass of ModuleLoadError
        - ModuleNotFound if module is not found
        - ModuleImportError if it is found, but cannot be imported

    Return: module object
    """
    path = []
    if pre_path:
        path.extend(pre_path.split(':'))
    if sys_path:
        path.extend(sys.path)
    if post_path:
        path.extend(post_path.split(':'))
    module_parts = module_name.split('.')
    for (i, part) in enumerate(module_parts):
        if i > 0:
            try:
                path = module.__path__
            except AttributeError:
                path = module.__name__

        try:
            module_info = imp.find_module(part, path)
        except ImportError, E:
            raise ModuleNotFound(part, path, E)

        name = ('.').join(module_parts[:i + 1])
        try:
            module = imp.load_module(name, *module_info)
        except ImportError, E:
            raise ModuleImportError(module_name, path, E, util.traceback())

    return module