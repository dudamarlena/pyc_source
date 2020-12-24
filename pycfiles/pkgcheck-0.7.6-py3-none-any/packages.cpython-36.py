# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/pkgcheck/pkgcheck/build/lib/pkgcheck/packages.py
# Compiled at: 2020-02-09 15:46:32
# Size of source mod 2**32: 1954 bytes
"""Various custom package objects."""
from pkgcore.ebuild import atom, cpv
from snakeoil import klass

class RawCPV:
    __doc__ = 'Raw CPV objects supporting basic restrictions/sorting.'
    __slots__ = ('category', 'package', 'fullver', 'version', 'revision')

    def __init__(self, category, package, fullver):
        self.category = category
        self.package = package
        self.fullver = fullver
        if self.fullver is not None:
            self.version, _, revision = self.fullver.partition('-r')
            self.revision = cpv._Revision(revision)
        else:
            self.revision = None
            self.version = None

    @property
    def key(self):
        return f"{self.category}/{self.package}"

    @property
    def versioned_atom(self):
        if self.fullver:
            return atom.atom(f"={self}")
        else:
            return atom.atom(str(self))

    @property
    def unversioned_atom(self):
        return atom.atom(self.key)

    def __lt__(self, other):
        return self.versioned_atom < other.versioned_atom

    def __str__(self):
        if self.fullver:
            return f"{self.category}/{self.package}-{self.fullver}"
        else:
            return f"{self.category}/{self.package}"

    def __repr__(self):
        address = '@%#8x' % (id(self),)
        return f"<{self.__class__.__name__} cpv={self.versioned_atom.cpvstr!r} {address}>"


class WrappedPkg:
    __doc__ = 'Generic package wrapper used to inject attributes into package objects.'
    __slots__ = ('_pkg', )

    def __init__(self, pkg):
        self._pkg = pkg

    def __str__(self):
        return str(self._pkg)

    def __repr__(self):
        return repr(self._pkg)

    def __lt__(self, other):
        return self.versioned_atom < other.versioned_atom

    __getattr__ = klass.GetAttrProxy('_pkg')
    __dir__ = klass.DirProxy('_pkg')


class FilteredPkg(WrappedPkg):
    __doc__ = 'Filtered package used to mark related results that should be skipped by default.'