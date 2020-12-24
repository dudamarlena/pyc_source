# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/pkgcheck/pkgcheck/build/lib/pkgcheck/checks/dropped_keywords.py
# Compiled at: 2020-02-09 15:46:32
# Size of source mod 2**32: 2538 bytes
from collections import defaultdict
from .. import addons, base, results, sources
from . import Check

class DroppedKeywords(results.VersionResult, results.Warning):
    __doc__ = 'Arch keywords dropped during version bumping.'

    def __init__(self, arches, **kwargs):
        (super().__init__)(**kwargs)
        self.arches = tuple(arches)

    @property
    def desc(self):
        return ', '.join(self.arches)


class DroppedKeywordsCheck(Check):
    __doc__ = 'Scan packages for keyword dropping across versions.'
    scope = base.package_scope
    _source = sources.PackageRepoSource
    required_addons = (addons.ArchesAddon,)
    known_results = frozenset([DroppedKeywords])

    def __init__(self, *args, arches_addon):
        (super().__init__)(*args)
        self.arches = frozenset(self.options.arches)

    def feed(self, pkgset):
        pkgset = [pkg for pkg in pkgset if not pkg.live]
        if len(pkgset) <= 1:
            return
        seen_arches = set()
        previous_arches = set()
        changes = defaultdict(list)
        for pkg in pkgset:
            pkg_arches = {x.lstrip('~-') for x in pkg.keywords}
            if '*' in pkg_arches:
                drops = set()
            else:
                drops = previous_arches.difference(pkg_arches) | seen_arches.difference(pkg_arches)
            for key in drops:
                if key in self.arches:
                    changes[key].append(pkg)

            if changes:
                disabled_arches = {x.lstrip('-') for x in pkg.keywords if x.startswith('-') if x.startswith('-')}
                adds = pkg_arches.difference(previous_arches) - disabled_arches
                for key in adds:
                    if key in changes:
                        del changes[key]

            seen_arches.update(pkg_arches)
            previous_arches = pkg_arches

        dropped = defaultdict(list)
        for key, pkgs in changes.items():
            if self.options.verbosity > 0:
                for pkg in pkgs:
                    dropped[pkg].append(key)

            else:
                dropped[pkgs[(-1)]].append(key)

        for pkg, keys in dropped.items():
            yield DroppedKeywords((sorted(keys)), pkg=pkg)