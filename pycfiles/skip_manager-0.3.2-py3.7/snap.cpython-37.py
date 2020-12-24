# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/skip/managers/snap.py
# Compiled at: 2019-07-12 16:27:22
# Size of source mod 2**32: 1486 bytes
from shutil import which
from subprocess import call
from typing import List, Dict
from skip.managers.manager import PackageManager

class Snap(PackageManager):

    @classmethod
    def remove(cls, packages: Dict[(str, List[str])]) -> bool:
        pass

    @classmethod
    def setup(cls) -> bool:
        pass

    @classmethod
    def command(cls) -> List[str]:
        return 'snap'.strip().split()

    @classmethod
    def install(cls, packages: Dict[(str, List[str])]) -> bool:
        print(cls.canonical_name() + ' packages: ' + str(packages))
        installed = True
        for package, flags in packages.items():
            cmd_lst = []
            cmd_lst.extend(cls.command())
            cmd_lst.extend(['install', package])
            cmd_lst.extend(flags)
            installed = installed and call(cmd_lst, stdin=True) == 0

        return installed

    @classmethod
    def canonical_name(cls) -> str:
        return 'snap'

    @classmethod
    def upgrade(cls) -> bool:
        cmd_lst = []
        cmd_lst.extend(cls.command())
        cmd_lst.extend(['refresh'])
        return call(cmd_lst, stdin=True) == 0

    @classmethod
    def clean(cls) -> bool:
        pass

    @classmethod
    def update(cls) -> bool:
        pass

    @classmethod
    def check(cls) -> bool:
        from skip.managers.manager import OperatingSystem
        return cls.operating_system() in {OperatingSystem.Linux} and which(cls.command()[0]) is not None