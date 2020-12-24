# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/pkgcheck/pkgcheck/build/lib/pkgcheck/checks/cleanup.py
# Compiled at: 2020-02-09 15:46:32
# Size of source mod 2**32: 2547 bytes
from snakeoil.strings import pluralism
from .. import base, results, sources
from . import Check

class RedundantVersion(results.VersionResult, results.Info):
    __doc__ = 'Redundant version(s) of a package in a specific slot.'

    def __init__(self, slot, later_versions, **kwargs):
        (super().__init__)(**kwargs)
        self.slot = slot
        self.later_versions = tuple(later_versions)

    @property
    def desc(self):
        s = pluralism(self.later_versions)
        versions = ', '.join(self.later_versions)
        return f"slot({self.slot}) keywords are overshadowed by version{s}: {versions}"


class RedundantVersionCheck(Check):
    __doc__ = 'Scan for overshadowed package versions.\n\n    Scan for versions that are likely shadowed by later versions from a\n    keywords standpoint (ignoring live packages that erroneously have\n    keywords).\n\n    Example: pkga-1 is keyworded amd64, pkga-2 is amd64.\n    pkga-1 can potentially be removed.\n    '
    scope = base.package_scope
    _source = sources.PackageRepoSource
    known_results = frozenset([RedundantVersion])

    def feed(self, pkgset):
        if len(pkgset) == 1:
            return
        stack = []
        bad = []
        for pkg in reversed(pkgset):
            if pkg.live:
                pass
            else:
                curr_set = {x for x in pkg.keywords if not x.startswith('-') if not x.startswith('-')}
                if not curr_set:
                    pass
                else:
                    matches = [ver for ver, keys in stack if ver.slot == pkg.slot if not curr_set.difference(keys)]
                    curr_set.update(['~' + x for x in curr_set if not x.startswith('~')])
                    stack.append([pkg, curr_set])
                    if matches:
                        bad.append((pkg, matches))

        for pkg, matches in reversed(bad):
            later_versions = (x.fullver for x in sorted(matches))
            yield RedundantVersion((pkg.slot), later_versions, pkg=pkg)