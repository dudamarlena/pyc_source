# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/skip/managers/pip.py
# Compiled at: 2019-07-12 16:27:22
# Size of source mod 2**32: 908 bytes
from shutil import which
from typing import List, Dict
from skip.managers.manager import PackageManager

class Pip(PackageManager):

    @classmethod
    def remove(cls, packages: Dict[(str, List[str])]) -> bool:
        pass

    @classmethod
    def command(cls) -> List[str]:
        return 'pip'.strip().split()

    @classmethod
    def canonical_name(cls) -> str:
        return 'pip'

    @classmethod
    def upgrade(cls) -> bool:
        pass

    @classmethod
    def clean(cls) -> bool:
        pass

    @classmethod
    def setup(cls):
        pass

    @classmethod
    def update(cls):
        pass

    @classmethod
    def check(cls) -> bool:
        from skip.managers.manager import OperatingSystem
        return cls.operating_system() in {OperatingSystem.Linux,
         OperatingSystem.MacOS} and which(cls.command()[0]) is not None