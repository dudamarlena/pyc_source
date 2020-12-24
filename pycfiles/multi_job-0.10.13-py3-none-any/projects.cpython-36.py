# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../multi_job/models/projects.py
# Compiled at: 2020-02-06 14:20:04
# Size of source mod 2**32: 471 bytes
from dataclasses import dataclass, field
from typing import List, Type, TypeVar
from multi_job.utils.strings import join_paths
T = TypeVar('T')

@dataclass
class Project:
    name: str
    path: str
    context: dict = field(default_factory=dict)

    def abs_path(self, config_path):
        return join_paths(config_path, self.path)

    @classmethod
    def from_config(cls: Type[T], dct: dict) -> List[T]:
        return [cls(name=k, **v) for k, v in dct.items()]