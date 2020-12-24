# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/skip/managers/mas.py
# Compiled at: 2019-07-12 16:27:22
# Size of source mod 2**32: 1109 bytes
from shutil import which
from subprocess import call
from typing import Dict, List
from skip.managers.manager import PackageManager

class Mas(PackageManager):

    @classmethod
    def install(cls, packages: Dict[(str, List[str])]) -> bool:
        pass

    @classmethod
    def clean(cls) -> bool:
        pass

    @classmethod
    def check(cls) -> bool:
        from skip.managers.manager import OperatingSystem
        return cls.operating_system() in {OperatingSystem.MacOS} and which(cls.command()[0]) is not None

    @classmethod
    def remove(cls, packages: Dict[(str, List[str])]) -> bool:
        pass

    @classmethod
    def canonical_name(cls) -> str:
        return 'mas'

    @classmethod
    def command(cls) -> List[str]:
        return 'mas'.strip().split()

    @classmethod
    def setup(cls) -> bool:
        pass

    @classmethod
    def update(cls) -> bool:
        pass

    @classmethod
    def upgrade(cls) -> bool:
        cmd_lst = cls.command()
        cmd_lst.extend(['upgrade'])
        return call(cmd_lst, stdin=True) == 0