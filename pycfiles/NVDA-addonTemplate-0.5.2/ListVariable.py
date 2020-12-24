# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Variables\ListVariable.py
# Compiled at: 2016-07-07 03:21:36
"""engine.SCons.Variables.ListVariable

This file defines the option type for SCons implementing 'lists'.

A 'list' option may either be 'all', 'none' or a list of names
separated by comma. After the option has been processed, the option
value holds either the named list elements, all list elements or no
list elements at all.

Usage example:

  list_of_libs = Split('x11 gl qt ical')

  opts = Variables()
  opts.Add(ListVariable('shared',
                      'libraries to build as shared libraries',
                      'all',
                      elems = list_of_libs))
  ...
  for lib in list_of_libs:
     if lib in env['shared']:
         env.SharedObject(...)
     else:
         env.Object(...)
"""
__revision__ = 'src/engine/SCons/Variables/ListVariable.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
__all__ = [
 'ListVariable']
import collections, SCons.Util

class _ListVariable(collections.UserList):

    def __init__(self, initlist=[], allowedElems=[]):
        collections.UserList.__init__(self, [ _f for _f in initlist if _f ])
        self.allowedElems = sorted(allowedElems)

    def __cmp__(self, other):
        raise NotImplementedError

    def __eq__(self, other):
        raise NotImplementedError

    def __ge__(self, other):
        raise NotImplementedError

    def __gt__(self, other):
        raise NotImplementedError

    def __le__(self, other):
        raise NotImplementedError

    def __lt__(self, other):
        raise NotImplementedError

    def __str__(self):
        if len(self) == 0:
            return 'none'
        else:
            self.data.sort()
            if self.data == self.allowedElems:
                return 'all'
            return (',').join(self)

    def prepare_to_store(self):
        return self.__str__()


def _converter(val, allowedElems, mapdict):
    """
    """
    if val == 'none':
        val = []
    elif val == 'all':
        val = allowedElems
    else:
        val = [ _f for _f in val.split(',') if _f ]
        val = [ mapdict.get(v, v) for v in val ]
        notAllowed = [ v for v in val if v not in allowedElems ]
        if notAllowed:
            raise ValueError('Invalid value(s) for option: %s' % (',').join(notAllowed))
    return _ListVariable(val, allowedElems)


def ListVariable(key, help, default, names, map={}):
    """
    The input parameters describe a 'package list' option, thus they
    are returned with the correct converter and validator appended. The
    result is usable for input to opts.Add() .

    A 'package list' option may either be 'all', 'none' or a list of
    package names (separated by space).
    """
    names_str = 'allowed names: %s' % (' ').join(names)
    if SCons.Util.is_List(default):
        default = (',').join(default)
    help = ('\n    ').join((
     help, '(all|none|comma-separated list of names)', names_str))
    return (key, help, default,
     None,
     lambda val: _converter(val, names, map))