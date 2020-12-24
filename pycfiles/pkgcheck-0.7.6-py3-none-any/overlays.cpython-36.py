# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/pkgcheck/pkgcheck/build/lib/pkgcheck/checks/overlays.py
# Compiled at: 2020-02-09 15:46:32
# Size of source mod 2**32: 5383 bytes
from snakeoil.sequences import iflatten_instance
from snakeoil.strings import pluralism
from .. import base, results, sources
from . import ExplicitlyEnabledCheck, OverlayRepoCheck, repo_metadata

class UnusedInMastersLicenses(results.VersionResult, results.Warning):
    __doc__ = "Licenses detected that are unused in the master repo(s).\n\n    In other words, they're likely to be removed so should be copied to the overlay.\n    "

    def __init__(self, licenses, **kwargs):
        (super().__init__)(**kwargs)
        self.licenses = tuple(licenses)

    @property
    def desc(self):
        s = pluralism(self.licenses)
        licenses = ', '.join(self.licenses)
        return f"unused license{s} in master repo(s): {licenses}"


class UnusedInMastersMirrors(results.VersionResult, results.Warning):
    __doc__ = "Mirrors detected that are unused in the master repo(s).\n\n    In other words, they're likely to be removed so should be copied to the overlay.\n    "

    def __init__(self, mirrors, **kwargs):
        (super().__init__)(**kwargs)
        self.mirrors = tuple(mirrors)

    @property
    def desc(self):
        s = pluralism(self.mirrors)
        mirrors = ', '.join(self.mirrors)
        return f"unused mirror{s} in master repo(s): {mirrors}"


class UnusedInMastersEclasses(results.VersionResult, results.Warning):
    __doc__ = "Eclasses detected that are unused in the master repo(s).\n\n    In other words, they're likely to be removed so should be copied to the overlay.\n    "

    def __init__(self, eclasses, **kwargs):
        (super().__init__)(**kwargs)
        self.eclasses = tuple(eclasses)

    @property
    def desc(self):
        es = pluralism((self.eclasses), plural='es')
        eclasses = ', '.join(self.eclasses)
        return f"unused eclass{es} in master repo(s): {eclasses}"


class UnusedInMastersGlobalUse(results.VersionResult, results.Warning):
    __doc__ = "Global USE flags detected that are unused in the master repo(s).\n\n    In other words, they're likely to be removed so should be copied to the overlay.\n    "

    def __init__(self, flags, **kwargs):
        (super().__init__)(**kwargs)
        self.flags = tuple(flags)

    @property
    def desc(self):
        s = pluralism(self.flags)
        flags = ', '.join(self.flags)
        return f"use.desc unused flag{s} in master repo(s): {flags}"


class UnusedInMastersCheck(repo_metadata._MirrorsCheck, OverlayRepoCheck, ExplicitlyEnabledCheck):
    __doc__ = 'Check for various metadata that may be removed from master repos.'
    scope = base.repo_scope
    _source = sources.RepositoryRepoSource
    known_results = frozenset([
     UnusedInMastersLicenses, UnusedInMastersMirrors, UnusedInMastersEclasses,
     UnusedInMastersGlobalUse])

    def start(self):
        self.unused_master_licenses = set()
        self.unused_master_mirrors = set()
        self.unused_master_eclasses = set()
        self.unused_master_flags = set()
        for repo in self.options.target_repo.masters:
            self.unused_master_licenses.update(repo.licenses)
            self.unused_master_mirrors.update(repo.mirrors.keys())
            self.unused_master_eclasses.update(repo.eclass_cache.eclasses.keys())
            self.unused_master_flags.update(flag for matcher, (flag, desc) in repo.config.use_desc)

        for repo in self.options.target_repo.masters:
            for pkg in repo:
                self.unused_master_licenses.difference_update(iflatten_instance(pkg.license))
                self.unused_master_mirrors.difference_update(self._get_mirrors(pkg))
                self.unused_master_eclasses.difference_update(pkg.inherited)
                self.unused_master_flags.difference_update(pkg.iuse_stripped.difference(pkg.local_use.keys()))

    def feed(self, pkg):
        if self.unused_master_licenses:
            pkg_licenses = set(iflatten_instance(pkg.license))
            licenses = self.unused_master_licenses & pkg_licenses
            if licenses:
                yield UnusedInMastersLicenses((sorted(licenses)), pkg=pkg)
            if self.unused_master_mirrors:
                pkg_mirrors = self._get_mirrors(pkg)
                mirrors = self.unused_master_mirrors & pkg_mirrors
                if mirrors:
                    yield UnusedInMastersMirrors((sorted(mirrors)), pkg=pkg)
            if self.unused_master_eclasses:
                pkg_eclasses = set(pkg.inherited)
                eclasses = self.unused_master_eclasses & pkg_eclasses
                if eclasses:
                    yield UnusedInMastersEclasses((sorted(eclasses)), pkg=pkg)
        else:
            if self.unused_master_flags:
                non_local_use = pkg.iuse_stripped.difference(pkg.local_use.keys())
                flags = self.unused_master_flags.intersection(non_local_use)
                if flags:
                    yield UnusedInMastersGlobalUse((sorted(flags)), pkg=pkg)