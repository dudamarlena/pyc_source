# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/skip/managers/brew.py
# Compiled at: 2019-07-12 16:27:22
# Size of source mod 2**32: 1773 bytes
from shutil import which
from subprocess import call
from typing import Dict, List
from skip.managers.manager import PackageManager

class Brew(PackageManager):

    @classmethod
    def clean(cls) -> bool:
        cmd_lst = cls.command()
        cmd_lst.extend(['cleanup'])
        return call(cmd_lst, stdin=True) == 0

    @classmethod
    def check(cls) -> bool:
        from skip.managers.manager import OperatingSystem
        return cls.operating_system() in {OperatingSystem.MacOS,
         OperatingSystem.Linux} and which(cls.command()[0]) is not None

    @classmethod
    def remove(cls, packages: Dict[(str, List[str])]) -> bool:
        pass

    @classmethod
    def canonical_name(cls) -> str:
        return 'brew'

    @classmethod
    def command(cls) -> List[str]:
        return 'brew'.strip().split()

    @classmethod
    def setup(cls) -> bool:
        pass

    @classmethod
    def install(cls, packages: Dict[(str, List[str])]) -> bool:
        print(cls.canonical_name() + ' packages: ' + str(packages))
        installed = True
        for package, flags in packages.items():
            cmd_lst = cls.command()
            cmd_lst.extend(['install', '--display-times', package])
            cmd_lst.extend(flags)
            installed = installed and call(cmd_lst, stdin=True) == 0

        return installed

    @classmethod
    def update(cls) -> bool:
        cmd_lst = cls.command()
        cmd_lst.extend(['update', '--force'])
        return call(cmd_lst, stdin=True) == 0

    @classmethod
    def upgrade(cls) -> bool:
        cmd_lst = cls.command()
        cmd_lst.extend(['upgrade', '--display-times'])
        return call(cmd_lst, stdin=True) == 0