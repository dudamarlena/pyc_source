# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/linjiao/dv/beim/beim/packages/factories/fromPyPackage.py
# Compiled at: 2013-12-08 21:45:16
"""
create a "packages" container from a python subpackage.
The python subpackage must contain a bunch of modules,
each of which describes a package.

In detail, we need:

bundles.py: packages are grouped into bundles. change it when new packages
            are added or when bundles need to be restructured
defaults.py: default packages to be installed
other modules: each module contains information about a specific package
    See beim.packages.Package for necessary attributes
"""

def factory(pypkg):
    bundles = _imp('bundles', pypkg)
    defaults = _imp('defaults', pypkg)
    packageSequence = []
    for name in bundles.bundleNames:
        packageSequence += bundles.bundleInfo[name]
        continue

    packageNames = packageSequence
    packageInfoTable = createTable(packageNames, pypkg)
    return Packages(packageInfoTable, packageNames)


def createTable(packageNames, pypkg):
    t = {}
    for name in packageNames:
        modname = name.replace('-', '_')
        m = _imp(modname, pypkg)
        t[name] = PackageProxy(m)
        continue

    return t


from ..Packages import Packages as base

class Packages(base):

    def __init__(self, name2package, names):
        self.name2package = name2package
        self.names = names

    def getAll(self):
        names = self.names
        return [ self.name2package[n] for n in names ]

    def getPackage(self, name):
        return self.name2package[name]


from beim.package.Package import Package

class PackageProxy(Package):
    """a proxy of a python module containing the
    information about a package acts like beim.package.Package
    """

    def __init__(self, module):
        self._module = module
        for k in ['name', 'deps', 'repo', 'patch']:
            v = getattr(module, k, None)
            setattr(self, k, v)

        return


def _imp(module, pypkg):
    name = pypkg.__name__
    m = '%s.%s' % (name, module)
    return __import__(m, {}, {}, [''])


__id__ = '$Id$'