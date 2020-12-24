# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/pkgcheck/pkgcheck/build/lib/pkgcheck/checks/stablereq.py
# Compiled at: 2020-02-09 15:46:32
# Size of source mod 2**32: 3782 bytes
from collections import defaultdict
from datetime import datetime
from itertools import chain
from snakeoil.klass import jit_attr
from snakeoil.strings import pluralism
from .. import base, git, results, sources
from . import GentooRepoCheck
day = 86400

class StableRequest(results.VersionResult, results.Info):
    __doc__ = 'Unstable package added over thirty days ago that could be stabilized.'

    def __init__(self, slot, keywords, age, **kwargs):
        (super().__init__)(**kwargs)
        self.slot = slot
        self.keywords = tuple(keywords)
        self.age = age

    @property
    def desc(self):
        s = pluralism(self.keywords)
        keywords = ', '.join(self.keywords)
        return f"slot({self.slot}) no change in {self.age} days for unstable keyword{s}: [ {keywords} ]"


class StableRequestCheck(GentooRepoCheck):
    __doc__ = "Ebuilds that have sat unstable with no changes for over a month.\n\n    By default, only triggered for arches with stable profiles. To check\n    additional arches outside the stable set specify them manually using the\n    -a/--arches option.\n\n    Note that packages with no stable keywords won't trigger this at all.\n    Instead they'll be caught by the UnstableOnly check.\n    "
    scope = base.package_scope
    _source = (sources.PackageRepoSource, (), (('source', sources.UnmaskedRepoSource),))
    required_addons = (git.GitAddon,)
    known_results = frozenset([StableRequest])

    def __init__(self, *args, git_addon=None):
        (super().__init__)(*args)
        self.today = datetime.today()
        self._git_addon = git_addon

    @jit_attr
    def modified_repo(self):
        return self._git_addon.cached_repo(git.GitModifiedRepo)

    def feed(self, pkgset):
        if self.modified_repo is None:
            return
        pkg_slotted = defaultdict(list)
        for pkg in pkgset:
            pkg_slotted[pkg.slot].append(pkg)

        pkg_keywords = set(chain.from_iterable(pkg.keywords for pkg in pkgset))
        stable_pkg_keywords = {x for x in pkg_keywords if x[0] not in frozenset({'-', '~'}) if x[0] not in frozenset({'-', '~'})}
        if stable_pkg_keywords:
            for slot, pkgs in sorted(pkg_slotted.items()):
                slot_keywords = set(chain.from_iterable(pkg.keywords for pkg in pkgs))
                stable_slot_keywords = slot_keywords.intersection(stable_pkg_keywords)
                for pkg in reversed(pkgs):
                    if not pkg.keywords:
                        pass
                    elif set(pkg.keywords).intersection(stable_pkg_keywords):
                        break
                    else:
                        try:
                            match = self.modified_repo.match(pkg.versioned_atom)[0]
                        except IndexError:
                            continue

                        added = datetime.strptime(match.date, '%Y-%m-%d')
                        days_old = (self.today - added).days
                        if days_old >= 30:
                            pkg_stable_keywords = {x.lstrip('~') for x in pkg.keywords}
                            if stable_slot_keywords:
                                keywords = stable_slot_keywords.intersection(pkg_stable_keywords)
                            else:
                                keywords = stable_pkg_keywords.intersection(pkg_stable_keywords)
                        keywords = sorted('~' + x for x in keywords)
                        yield StableRequest(slot, keywords, days_old, pkg=pkg)
                        break