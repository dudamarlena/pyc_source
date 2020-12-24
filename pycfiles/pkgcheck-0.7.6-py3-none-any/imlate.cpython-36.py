# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/pkgcheck/pkgcheck/build/lib/pkgcheck/checks/imlate.py
# Compiled at: 2020-02-09 15:46:32
# Size of source mod 2**32: 4781 bytes
from collections import defaultdict
from itertools import chain
from pkgcore.restrictions import packages, values
from snakeoil.strings import pluralism
from .. import addons, base, results, sources
from . import Check

class PotentialStable(results.VersionResult, results.Info):
    __doc__ = 'Stable arches with potential stable package candidates.'

    def __init__(self, slot, stable, keywords, **kwargs):
        (super().__init__)(**kwargs)
        self.slot = slot
        self.stable = tuple(stable)
        self.keywords = tuple(keywords)

    @property
    def desc(self):
        es = pluralism((self.stable), plural='es')
        stable = ', '.join(self.stable)
        s = pluralism(self.keywords)
        keywords = ', '.join(self.keywords)
        return f"slot({self.slot}), stabled arch{es}: [ {stable} ], potential{s}: [ {keywords} ]"


class LaggingStable(results.VersionResult, results.Info):
    __doc__ = 'Stable arches for stabilized package that are lagging from a stabling standpoint.'

    def __init__(self, slot, stable, keywords, **kwargs):
        (super().__init__)(**kwargs)
        self.slot = slot
        self.stable = tuple(stable)
        self.keywords = tuple(keywords)

    @property
    def desc(self):
        es = pluralism((self.stable), plural='es')
        stable = ', '.join(self.stable)
        keywords = ', '.join(self.keywords)
        return f"slot({self.slot}), stabled arch{es}: [ {stable} ], lagging: [ {keywords} ]"


class ImlateCheck(Check):
    __doc__ = 'Scan for ebuilds that are lagging in stabilization.'
    scope = base.package_scope
    _source = sources.PackageRepoSource
    required_addons = (addons.StableArchesAddon,)
    known_results = frozenset([PotentialStable, LaggingStable])

    @staticmethod
    def mangle_argparser(parser):
        parser.plugin.add_argument('--source-arches',
          action='csv', metavar='ARCH', help='comma separated list of arches to compare against for lagging stabilization',
          docs='\n                Comma separated list of arches to compare against for\n                lagging stabilization.\n\n                The default arches are all stable arches (unless --arches is specified).\n            ')

    def __init__(self, *args, stable_arches_addon=None):
        (super().__init__)(*args)
        self.all_arches = frozenset(self.options.arches)
        self.stable_arches = frozenset(arch.strip().lstrip('~') for arch in self.options.stable_arches)
        self.target_arches = frozenset(f"~{arch}" for arch in self.stable_arches)
        source_arches = self.options.source_arches
        if source_arches is None:
            source_arches = self.options.stable_arches
        self.source_arches = frozenset(arch.lstrip('~') for arch in source_arches)
        self.source_filter = packages.PackageRestriction('keywords', values.ContainmentMatch2(self.source_arches))

    def feed(self, pkgset):
        pkg_slotted = defaultdict(list)
        for pkg in pkgset:
            pkg_slotted[pkg.slot].append(pkg)

        fmatch = self.source_filter.match
        for slot, pkgs in sorted(pkg_slotted.items()):
            slot_keywords = set(chain.from_iterable(pkg.keywords for pkg in pkgs))
            stable_slot_keywords = self.all_arches.intersection(slot_keywords)
            potential_slot_stables = {'~' + x for x in stable_slot_keywords}
            newer_slot_stables = set()
            for pkg in reversed(pkgs):
                if not fmatch(pkg):
                    newer_slot_stables.update(self.all_arches.intersection(pkg.keywords))
                else:
                    stable = {'~' + x for x in self.source_arches.intersection(pkg.keywords)}
                    lagging = potential_slot_stables.intersection(pkg.keywords)
                    lagging -= {'~' + x for x in newer_slot_stables}
                    lagging -= stable
                    if lagging:
                        stable_kwds = (x for x in pkg.keywords if x[0] not in ('~',
                                                                               '-'))
                        yield LaggingStable(slot,
                          (sorted(stable_kwds)), (sorted(lagging)), pkg=pkg)
                    unstable_keywords = {x for x in pkg.keywords if x[0] == '~' if x[0] == '~'}
                    potential = self.target_arches.intersection(unstable_keywords)
                    potential -= lagging | stable
                    if potential:
                        stable_kwds = (x for x in pkg.keywords if x[0] not in ('~',
                                                                               '-'))
                        yield PotentialStable(slot,
                          (sorted(stable_kwds)), (sorted(potential)), pkg=pkg)
                    break