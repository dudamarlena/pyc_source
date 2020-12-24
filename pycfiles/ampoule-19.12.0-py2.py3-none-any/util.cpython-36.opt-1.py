# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /ampoule/util.py
# Compiled at: 2017-12-10 09:58:00
# Size of source mod 2**32: 1349 bytes
"""
some utilities
"""
import os, sys, __main__
from twisted.python.filepath import FilePath
from twisted.python.reflect import namedAny

def findPackagePath(modulePath):
    """
    Try to find the sys.path entry from a modulePath object, simultaneously
    computing the module name of the targetted file.
    """
    p = modulePath
    l = [p.basename().split('.')[0]]
    while p.parent() != p:
        for extension in ('py', 'pyc', 'pyo', 'pyd', 'dll'):
            sib = p.sibling('__init__.' + extension)
            if sib.exists():
                p = p.parent()
                l.insert(0, p.basename())
                break
        else:
            return (
             p.parent(), '.'.join(l))


def mainpoint(function):
    """
    Decorator which declares a function to be an object's mainpoint.
    """
    if function.__module__ == '__main__':
        p = FilePath(__main__.__file__)
        p, mn = findPackagePath(p)
        pname = p.path
        if pname not in map(os.path.abspath, sys.path):
            sys.path.insert(0, pname)
        exitcode = namedAny(mn + '.' + function.__name__)(sys.argv)
        if exitcode is None:
            exitcode = 0
        sys.exit(exitcode)
    return function