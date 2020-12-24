# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/skip/managers/npm.py
# Compiled at: 2019-07-12 16:27:22
# Size of source mod 2**32: 1525 bytes
from shutil import which
from subprocess import call
from typing import List, Dict
from skip.managers.manager import OperatingSystem
from skip.managers.manager import PackageManager

class Npm(PackageManager):

    @classmethod
    def remove(cls, packages: Dict[(str, List[str])]) -> bool:
        pass

    @classmethod
    def canonical_name(cls) -> str:
        return 'npm'

    @classmethod
    def command(cls) -> List[str]:
        return 'npm'.strip().split()

    @classmethod
    def upgrade(cls):
        pass

    @classmethod
    def clean(cls) -> bool:
        pass

    @classmethod
    def setup(cls):
        pass

    @classmethod
    def install(cls, packages: Dict[(str, List[str])]):
        print(cls.canonical_name() + ' packages: ' + str(packages))
        installed = True
        for package, flags in packages.items():
            cmd_lst = cls.command()
            cmd_lst.extend(['install', '-g', package])
            cmd_lst.extend(flags)
            installed = installed and call(cmd_lst, stdin=True) == 0

        return installed

    @classmethod
    def update(cls):
        cmd_lst = cls.command()
        cmd_lst.extend(['update', '-g'])
        return call(cmd_lst, stdin=True) == 0

    @classmethod
    def check(cls) -> bool:
        return cls.operating_system() in {OperatingSystem.MacOS,
         OperatingSystem.Linux} and which(cls.command()[0]) is not None