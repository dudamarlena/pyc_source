# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/fileinfo/investigator.py
# Compiled at: 2009-05-08 07:02:41
"""Abstract base class for file investigators.

An investigator has a dict. attribute 'attrMap', which maps
attr. names or regular expresions to method names.
"""
import sys, time, datetime, os.path, stat, re
from os.path import isdir, isfile, islink, getsize, isabs, getmtime
if sys.platform == 'darwin':
    try:
        from Carbon.File import FSResolveAliasFile, FSRef
        HAVE_CARBON = True
    except ImportError:
        HAVE_CARBON = False

if sys.platform == 'darwin' and HAVE_CARBON:

    def isAlias(path):
        """Is this a Carbon alias file?"""
        return bool(FSRef(path).FSIsAliasFile()[0])


    os.path.isalias = isAlias

def getSum(attrName, recs):
    """Return sum of a given attribute name for a list of records."""
    total = 0
    for r in recs:
        s = getattr(r, attrName)
        if s != 'n/a':
            total += s

    return total


class BaseInvestigator(object):
    """An abstract class for determining attributes of files."""
    __module__ = __name__
    attrMap = {}
    totals = ()

    def __init__(self, path):
        self.path = path

    def activate(self):
        """Try activating self, setting 'active' variable."""
        self.active = False
        return self.active

    def getFunc(self, attrName):
        """Return access method for attribute named 'attrName'."""
        funcName = self.attrMap[attrName]
        return getattr(self, funcName)

    def getAttrValue(self, attrName):
        """Return value for attribute named 'attrName'."""
        if attrName in self.attrMap.keys():
            funcName = self.attrMap[attrName]
            if funcName == None:
                return
            return getattr(self, funcName)()
        else:
            matchingAttrNames = [ an for an in self.attrMap.keys() if re.match(an, attrName) ]
            if matchingAttrNames:
                funcName = self.attrMap[matchingAttrNames[0]]
                return getattr(self, funcName)(attrName)
        return