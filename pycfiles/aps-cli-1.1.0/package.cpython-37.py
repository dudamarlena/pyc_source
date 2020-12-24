# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python3.7/site-packages/aprt/package.py
# Compiled at: 2019-08-02 08:01:39
# Size of source mod 2**32: 9554 bytes
from enum import Enum, unique
import operator
from . import util
from .version import Version

@unique
class Constraint(Enum):
    eq = 0
    gt = 1
    lt = 2
    ge = 3
    le = 4

    @classmethod
    def parse(cls, string):
        if string == '=':
            return cls.eq
        if string == '>':
            return cls.gt
        if string == '<':
            return cls.lt
        if string == '>=':
            return cls.ge
        if string == '<=':
            return cls.le
        if string == '==':
            return cls.eq
        raise ValueError("Invalid constraint `{}'.".format(string))

    def __str__(self):
        if self is self.__class__.eq:
            return '='
        if self is self.__class__.gt:
            return '>'
        if self is self.__class__.lt:
            return '<'
        if self is self.__class__.ge:
            return '>='
        if self is self.__class__.le:
            return '<='
        raise ValueError("Invalid constraint value `{}'.".format(self.value))

    def functor(self):
        if self is self.__class__.eq:
            return operator.eq
        if self is self.__class__.gt:
            return operator.gt
        if self is self.__class__.lt:
            return operator.lt
        if self is self.__class__.ge:
            return operator.ge
        if self is self.__class__.le:
            return operator.le


class Dependency:
    """Dependency"""

    def __init__(self, name, constraint=None, version=None):
        self.name = name
        self.version = version
        self.constraint = constraint

    def satisfiedBy(self, package):
        if self.constraint is None:
            return self.name == package.name
        return self.name == package.name and self.constraint.toFunctor(package.version(), self.version)

    @classmethod
    def parse(cls, blob):
        constraint_start = util.find_if(blob, lambda x: util.is_one_of(x, ['=', '>', '<']))
        if constraint_start < 0:
            return cls(blob)
        version_start = util.find_if(blob[constraint_start + 1:], lambda x: not util.is_one_of(x, ['=', '>', '<']))
        if version_start < 0:
            raise ValueError("Failed to parse dependency: constraint specified without version in `{}'".format(blob))
        version_start += constraint_start + 1
        name = blob[0:constraint_start]
        constraint = blob[constraint_start:version_start]
        version = blob[version_start:]
        return cls(name, Constraint.parse(constraint), Version.parse(version))

    def __str__(self):
        if self.constraint is None:
            return self.name
        return '{}{}{}'.format(self.name, self.constraint, self.version)

    def __repr__(self):
        return self.__str__()


class Package:
    """Package"""

    def __init__(self, name):
        self.name = name
        self.data = {'pkgname': [name]}

    def __make_key(self, key):
        if key not in self.data:
            self.data[key] = []

    def add_value(self, key, value):
        self._Package__make_key(key)
        self.data[key].append(value)

    def add_values(self, key, values):
        self._Package__make_key(key)
        self.data[key] += values

    def get_value(self, key):
        if key not in self.data:
            return
        return self.data[key][0]

    def get_values(self, key):
        if key not in self.data:
            return []
        return self.data[key]

    def version(self):
        return Version(self.get_value('pkgver'), self.get_value('pkgrel'), self.get_value('epoch'))

    def depends(self):
        return map(Dependency.parse, self.get_values('depends'))

    def optdepends(self):
        return map(Dependency.parse, self.get_values('optdepends'))

    def makedepends(self):
        return map(Dependency.parse, self.get_values('makedepends'))

    def checkdepends(self):
        return map(Dependency.parse, self.get_values('checkdepends'))

    def alldepends(self):
        yield from self.depends()
        yield from self.makedepends()
        yield from self.checkdepends()
        if False:
            yield None

    def installed(self):
        return map(package_from_name_guess, self.get_values('installed'))

    def provides(self):
        result = set(map(Dependency.parse, self.get_values('provides')))
        result.add(Dependency.parse(self.name))
        return result

    def providesName(self, name):
        for provide in self.provides():
            if provide.name == name:
                return True

        return False

    def conflicts(self):
        return map(Dependency.parse, self.get_values('conflicts'))

    def replaces(self):
        return map(Dependency.parse, self.get_values('replaces'))

    def hasOption(self, option):
        return option in self.get_values('options')

    def __str__(self):
        return '{}-{}'.format(self.name, str(self.version()))

    def __repr__(self):
        return '{{Package: {}, version: {}}}'.format(self.name, str(self.version()))

    def split_debug_package(self) -> 'Package':
        """
                Generate a split debug package based on an existing package.

                This creates a package definition as created by makepkg when
                the debug and split options are given.
                """
        use_fields = ('pkgbase', 'pkgver', 'url', 'builddate', 'packager', 'size',
                      'arch', 'license', 'makedepends', 'checkdepends')
        package = Package(self.name + '-debug')
        package.add_value('pkgdesc', 'Detached debugging symbols for {}'.format(self.name))
        for key, values in self.data.items():
            if key not in use_fields:
                continue
            package.add_values(key, values)

        return package


def split_pkgname(name):
    """
                Split a package name in four fields:
                (name, pkgver, pkgrel, epoch)
        """
    base, sep, pkgrel = name.rpartition('-')
    name, sep, pkgver = base.rpartition('-')
    epoch, sep, pkgver = pkgver.partition(':')
    if not sep:
        epoch, pkgver = None, epoch
    else:
        epoch = int(epoch)
    return (name, pkgver, pkgrel, epoch)


def split_pkgname_arch(name):
    """
                Split a package name with architecture in five fields:
                (name, pkgver, pkgrel, epoch, arch)
        """
    rest, sep, arch = name.rpartition('-')
    name, pkgver, pkgrel, epoch = split_pkgname(rest)
    return (
     name, pkgver, pkgrel, epoch, arch)


def package_from_name(name):
    name, pkgver, pkgrel, epoch = split_pkgname(name)
    package = Package(name)
    package.add_value('pkgver', pkgver)
    package.add_value('pkgrel', pkgrel)
    package.add_value('epoch', epoch)
    return package


def package_from_name_arch(name):
    name, pkgver, pkgrel, epoch, arch = split_pkgname_arch(name)
    package = Package(name)
    package.add_value('pkgver', pkgver)
    package.add_value('pkgrel', pkgrel)
    package.add_value('epoch', epoch)
    package.add_value('arch', arch)
    return package


def package_from_name_guess(name):
    _, _, arch = name.rpartition('-')
    if arch in ('any', 'x86_64', 'i686'):
        return package_from_name_arch(name)
    return package_from_name(name)


def neighbour_table(packages):
    """
        Build a neighbour table for dependencies.
        """
    table = {}
    for package in packages:
        table[package.name] = [x.name for x in package.alldepends()]
        for name in map(lambda x: x.name, package.provides()):
            table[package.name] = list(table[package.name])

    return table


def reverse_neighbour_table(packages):
    """
        Build a neighbour table for reverse dependencies.
        """
    table = {}
    for package in packages:
        if package.name not in table:
            table[package.name] = set()
        for dependency in package.alldepends():
            if dependency.name not in table:
                table[dependency.name] = set()
            for provides in [package.name] + [x.name for x in package.provides()]:
                table[dependency.name].add(package.name)

    return table


def reachability_table(neighbours):
    """
        Build a reachability table from a neighbour table.
        """
    reachable = neighbours.copy()
    for a in reachable:
        for b in reachable:
            if a in reachable[b]:
                reachable[b].update(reachable[a])

    return reachable


def reverse_dependencies(database, packages, recursive=True):
    """
        Get a set of reverse dependencies for a list of packages.
        If recursive is true indirect reverse dependencies are also given.
        """
    reverse_dependencies = build_reverse_neighbour_table(database)
    if recursive:
        reverse_dependencies = reachability_table(reverse_dependencies)
    result = set()
    for package in packages:
        result.update(reverse_dependencies[package])

    return result