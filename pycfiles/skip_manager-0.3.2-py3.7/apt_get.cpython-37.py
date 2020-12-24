# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/skip/managers/apt_get.py
# Compiled at: 2019-07-12 16:27:22
# Size of source mod 2**32: 1952 bytes
from shutil import which
from subprocess import call
from typing import List, Dict
from skip.managers.manager import PackageManager, OperatingSystem

class AptGet(PackageManager):

    @classmethod
    def remove(cls, packages: Dict[(str, List[str])]) -> bool:
        cmd_lst = ['sudo', '-E']
        cmd_lst.extend(cls.command())
        cmd_lst.extend(['update', '-y'])
        return call(cmd_lst, stdin=True) == 0

    @classmethod
    def command(cls) -> List[str]:
        return 'apt-get'.strip().split()

    @classmethod
    def install(cls, packages: Dict[(str, List[str])]) -> bool:
        print(cls.canonical_name() + ' packages: ' + str(packages))
        installed = True
        for package, flags in packages.items():
            cmd_lst = [
             'sudo', '-E']
            cmd_lst.extend(cls.command())
            cmd_lst.extend(['install', package, '-y'])
            cmd_lst.extend(flags)
            installed = installed and call(cmd_lst, stdin=True) == 0

        return installed

    @classmethod
    def canonical_name(cls) -> str:
        return 'apt-get'

    @classmethod
    def upgrade(cls) -> bool:
        cmd_lst = ['sudo', '-E']
        cmd_lst.extend(cls.command())
        cmd_lst.extend(['dist-upgrade', '-y'])
        return call(cmd_lst, stdin=True) == 0

    @classmethod
    def clean(cls) -> bool:
        cmd_lst = ['sudo', '-E']
        cmd_lst.extend(cls.command())
        cmd_lst.extend(['autoclean', '-y'])
        return call(cmd_lst, stdin=True) == 0

    @classmethod
    def setup(cls):
        pass

    @classmethod
    def update(cls):
        cmd_lst = [
         'sudo', '-E']
        cmd_lst.extend(cls.command())
        cmd_lst.extend(['update', '-y'])
        return call(cmd_lst, stdin=True) == 0

    @classmethod
    def check(cls) -> bool:
        return cls.operating_system() in {OperatingSystem.Linux} and which(cls.command()[0]) is not None