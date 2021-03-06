# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joel/Workspace/multi-job/models/routines.py
# Compiled at: 2020-02-05 13:19:08
# Size of source mod 2**32: 427 bytes
from dataclasses import dataclass
from typing import List, Type, TypeVar
from .jobs import Job
T = TypeVar('T')

@dataclass
class Routine:
    name: str
    jobs: List[str]

    def resolve_jobs(self, jobs: List[Job]) -> List[Job]:
        return [j for j in jobs if j.name in self.jobs]

    @classmethod
    def from_config(cls: Type[T], dct: dict) -> List[T]:
        return [cls(name=k, jobs=v) for k, v in dct.items()]