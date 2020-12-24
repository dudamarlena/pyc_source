# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/fileinfo/plugging.py
# Compiled at: 2008-06-07 18:03:57
"""Simple plug-in mechanim.

"""
import sys, glob, os, os.path
from os.path import dirname, basename, abspath, pathsep, join, splitext

def getPluginsFromModule(mod, baseClass):
    """Return all plug-in classes contained in a loaded module."""
    res = [ obj for (name, obj) in mod.__dict__.items() if type(obj) == type if obj != baseClass if issubclass(obj, baseClass) ]
    return res


def loadPlugins(baseClass, filenamePattern, folder=None, envVar=None):
    """Search, load oad and return list of plugin classes from known places."""
    paths = []
    if folder != None:
        paths = [
         folder]
    if envVar and envVar in os.environ:
        paths += os.environ[envVar].split(os.path.pathsep)
    plugins = []
    for path in paths:
        modPaths = glob.glob(join(path, filenamePattern))
        for mp in modPaths:
            dn = dirname(mp)
            mn = basename(splitext(mp)[0])
            sys.path.insert(0, dn)
            mod = __import__(mn)
            invs = getPluginsFromModule(mod, baseClass)
            del sys.path[0]
            plugins += invs

    return plugins