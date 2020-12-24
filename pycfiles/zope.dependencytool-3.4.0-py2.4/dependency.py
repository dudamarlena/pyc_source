# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zope/dependencytool/dependency.py
# Compiled at: 2007-09-21 15:26:02
"""Basic dependency representation.

$Id: dependency.py 27164 2004-08-17 11:16:39Z hdima $
"""

class Dependency(object):
    """Object representing a dependency."""
    __module__ = __name__

    def __init__(self, name, file, lineno):
        """Initialize a Dependency instance.

        name -- dotted name of the module

        file -- full path of a source file that depends on the module
        named by `name`

        lineno -- line number within file where the dependency was
        identified (import or ZCML reference)

        """
        self.name = name
        self.occurences = [(file, lineno)]

    def addOccurence(self, file, lineno):
        """Add occurenace of the dependency in the code."""
        self.occurences.append((file, lineno))

    def isSubPackageOf(self, dep):
        """Return True if this dependency's module is a sub-package of dep."""
        return self.name.startswith(dep.name + '.')

    def __cmp__(self, other):
        """Compare dependecies by module name."""
        return cmp(self.name, other.name)