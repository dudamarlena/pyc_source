# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/runner/work/pkgcheck/pkgcheck/build/lib/pkgcheck/checks/acct.py
# Compiled at: 2020-02-09 15:46:32
# Size of source mod 2**32: 3879 bytes
"""Various checks for acct-group and acct-user packages."""
import re
from collections import defaultdict
from functools import partial
from itertools import chain
from pkgcore.ebuild import restricts
from pkgcore.restrictions import packages
from .. import base, results, sources
from . import Check

class MissingAccountIdentifier(results.VersionResult, results.Warning):
    __doc__ = 'UID/GID can not be found in account package.'

    def __init__(self, var, **kwargs):
        (super().__init__)(**kwargs)
        self.var = var

    @property
    def desc(self):
        return f"unable to determine the value of {self.var} variable"


class ConflictingAccountIdentifiers(results.Error):
    __doc__ = 'Same UID/GID is used by multiple packages.'

    def __init__(self, kind, identifier, pkgs):
        super().__init__()
        self.kind = kind
        self.identifier = identifier
        self.pkgs = tuple(pkgs)

    @property
    def desc(self):
        return f"conflicting {self.kind} id {self.identifier} usage: [ {', '.join(self.pkgs)} ]"


class OutsideRangeAccountIdentifier(results.VersionResult, results.Error):
    __doc__ = 'UID/GID outside allowed allocation range.'

    def __init__(self, kind, identifier, **kwargs):
        (super().__init__)(**kwargs)
        self.kind = kind
        self.identifier = identifier

    @property
    def desc(self):
        return f"{self.kind} id {self.identifier} outside permitted static allocation range (0..499, 60001+)"


class AcctCheck(Check):
    __doc__ = 'Various checks for acct-* packages.\n\n    Verify that acct-* packages do not use conflicting, invalid or out-of-range\n    UIDs/GIDs.\n    '
    scope = base.repo_scope
    _restricted_source = (sources.RestrictionRepoSource,
     (
      (packages.OrRestriction)(restricts.CategoryDep('acct-user'), restricts.CategoryDep('acct-group')*()),))
    _source = (sources.RepositoryRepoSource, (), (('source', _restricted_source),))
    known_results = frozenset([
     MissingAccountIdentifier, ConflictingAccountIdentifiers,
     OutsideRangeAccountIdentifier])

    def __init__(self, *args):
        (super().__init__)(*args)
        self.id_re = re.compile('ACCT_(?P<var>USER|GROUP)_ID=(?P<quot>[\\\'"]?)(?P<id>[0-9]+)(?P=quot)')
        self.seen_uids = defaultdict(partial(defaultdict, list))
        self.seen_gids = defaultdict(partial(defaultdict, list))
        self.category_map = {'acct-user':(
          self.seen_uids, 'USER', (65534, )), 
         'acct-group':(
          self.seen_gids, 'GROUP', (65533, 65534))}

    def feed(self, pkg):
        try:
            seen_id_map, expected_var, extra_allowed_ids = self.category_map[pkg.category]
        except KeyError:
            return
        else:
            for l in pkg.ebuild.text_fileobj():
                m = self.id_re.match(l)
                if m is not None:
                    if m.group('var') == expected_var:
                        found_id = int(m.group('id'))
                        break
            else:
                yield MissingAccountIdentifier(f"ACCT_{expected_var}_ID", pkg=pkg)
                return

            if found_id >= 500:
                if found_id not in extra_allowed_ids:
                    yield OutsideRangeAccountIdentifier((expected_var.lower()), found_id, pkg=pkg)
                    return
            seen_id_map[found_id][pkg.key].append(pkg)

    def finish(self):
        for seen, expected_var, _ids in self.category_map.values():
            for found_id, pkgs in sorted(seen.items()):
                if len(pkgs) > 1:
                    pkgs = (x.cpvstr for x in sorted(chain.from_iterable(pkgs.values())))
                    yield ConflictingAccountIdentifiers(expected_var.lower(), found_id, pkgs)