# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\PROJECT_HOME\bets-cli\src\bets\model\stats\abstract_stats.py
# Compiled at: 2019-05-15 20:04:33
# Size of source mod 2**32: 726 bytes
from typing import Dict, List, Union
from tabulate import tabulate

class AbstractStats:
    KEYS: List[str]

    def __getitem__(self, key: str):
        try:
            return self.__dict__[key]
        except KeyError:
            if hasattr(self, key):
                return getattr(self, key)
            raise

    def __repr__(self):
        return repr(self.as_dict())

    def __str__(self):
        return tabulate([self.as_dict()], headers='keys', floatfmt='.02f', stralign='right')

    def as_tuple(self) -> tuple:
        return tuple((self[key] for key in self.KEYS))

    def as_dict(self) -> Dict[(str, Union[(int, float, str)])]:
        return {key:self[key] for key in self.KEYS}