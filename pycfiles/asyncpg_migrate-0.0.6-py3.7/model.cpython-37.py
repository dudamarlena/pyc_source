# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/asyncpg_migrate/model.py
# Compiled at: 2020-01-13 09:51:39
# Size of source mod 2**32: 3641 bytes
import copy
from dataclasses import dataclass, field
import datetime as dt, enum
from pathlib import Path
import typing as t, asyncpg
Timestamp = t.NewType('Timestamp', dt.datetime)
MigrationCallable = t.Callable[([asyncpg.Connection],
 t.Callable[([asyncpg.Connection],
  t.Coroutine[(t.Any,
   t.Any,
   None)])])]

class Revision(int):

    @classmethod
    def decode(cls, rev: t.Union[(str, int, 'Revision')], all_revisions: t.Sequence['Revision']=None) -> 'Revision':
        if isinstance(rev, Revision):
            return rev
            if isinstance(rev, int):
                if rev >= 0:
                    return Revision(rev)
                raise ValueError('Decoding from negative value is not possible')
        else:
            try:
                return cls.decode(int(rev))
            except ValueError:
                if not all_revisions:
                    raise ValueError('Decoding from "head" or "base" require knowing all revisions')
                if rev.lower() == 'head':
                    return all_revisions[(-1)]
                if rev.lower() == 'base':
                    return all_revisions[0]
                raise ValueError(f'{rev} is neither "base" nor "head" and thus cannot be converted from string')


class MigrationDir(str, enum.Enum):
    UP = 'UP'
    DOWN = 'DOWN'


class Migrations(t.Dict[(Revision, 'Migration')]):

    def slice(self, start: int, end: t.Optional[int]=None) -> 'Migrations':
        real_end = len(self) if end is None else end
        if start > real_end:
            raise ValueError(f"Cannot slice if end={end} < start={start}")
        if start == 1:
            if real_end == len(self):
                return copy.deepcopy(self)
        new_migrations = Migrations()
        for r in range(start, real_end + 1, 1):
            revision = Revision(r)
            new_migrations[revision] = self[revision]

        return new_migrations

    def upgrade_iterator(self) -> t.Iterator['Migration']:
        return iter([self[rev] for rev in sorted(self)])

    def downgrade_iterator(self) -> t.Iterator['Migration']:
        return iter([self[rev] for rev in sorted(self, reverse=True)])

    def revisions(self) -> t.Sequence[Revision]:
        return sorted(self.keys())


@dataclass(frozen=True)
class Migration:
    revision: Revision
    label: str
    path: Path
    upgrade = field(hash=False,
      compare=False)
    upgrade: MigrationCallable
    downgrade = field(hash=False,
      compare=False)
    downgrade: MigrationCallable


@dataclass(frozen=True)
class MigrationHistoryEntry:
    revision = field(hash=True, compare=True)
    revision: Revision
    timestamp = field(hash=True, compare=True)
    timestamp: Timestamp
    direction = field(hash=True, compare=True)
    direction: MigrationDir
    label = field(hash=False, compare=False)
    label: str


class MigrationHistory(t.List[MigrationHistoryEntry]):
    pass


@dataclass(frozen=True)
class Config:
    script_location: Path
    database_dsn = field(repr=False)
    database_dsn: str
    database_name: str