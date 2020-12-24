# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/find_home.py
# Compiled at: 2008-03-29 07:17:18
"""This lets you find files with just a path name relative to where
the program's executable code script sits."""
import sys
_scriptname = sys.argv[0]
import os
__version__ = '$Revision: 1.6 $'

def _searchdir(pathlist, s, access):
    for t in pathlist:
        if t == '':
            t = '.'
        tmp = '%s/%s' % (t, s)
        if os.access(tmp, access) and os.path.isdir(tmp):
            return tmp

    raise RuntimeError, "Can't find %s" % s


def _search(pathlist, s, access):
    for t in pathlist:
        if t == '':
            t = '.'
        tmp = '%s/%s' % (t, s)
        if os.access(tmp, access):
            return tmp

    raise RuntimeError, "Can't find %s" % s


def executable(s, general=True):
    """Find an executable program.
        It searches first in the directory of the currently executing
        python script.  Optionally, it then looks at PATH.
        If general=False, the function should fail unless
        the executable is in the same directory as the currently
        executing python script."""
    p = [
     os.path.dirname(_scriptname)]
    if general:
        p.extend(os.environ['PATH'].split(':'))
    return _search(p, s, os.X_OK)


def module(s, general=True):
    """Find a module. Returns pathname."""
    p = [
     os.path.dirname(_scriptname)]
    if general:
        p.extend(sys.path)
    return _search(p, '%s.py' % s, os.R_OK)


def os_prgm(nm, general=1):
    """Find an operating-system dependent executable program."""
    return executable('bin__' + os.uname()[0] + '/' + nm, general)


def data(s):
    """Find a data file."""
    p = [
     '.', os.path.dirname(_scriptname)]
    return _search(p, s, os.R_OK)


def directory(s):
    """Find a directory."""
    p = [
     os.path.dirname(_scriptname)]
    return _searchdir(p, s, os.X_OK)


assert __name__ == '__main__' and data('find_home.py')