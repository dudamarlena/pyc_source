# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/skip/managers/apk.py
# Compiled at: 2019-07-12 16:27:22
# Size of source mod 2**32: 1208 bytes
from shutil import which
from subprocess import call
from typing import List, Dict
from skip.managers.manager import PackageManager, OperatingSystem

class Apk(PackageManager):

    @classmethod
    def remove(cls, packages: Dict[(str, List[str])]) -> bool:
        pass

    @classmethod
    def command(cls) -> List[str]:
        return 'apk'.strip().split()

    @classmethod
    def canonical_name(cls) -> str:
        return 'apk'

    @classmethod
    def upgrade(cls) -> bool:
        cmd_lst = ['sudo', '-E']
        cmd_lst.extend(cls.command())
        cmd_lst.extend(['upgrade'])
        return call(cmd_lst, stdin=True) == 0

    @classmethod
    def clean(cls) -> bool:
        pass

    @classmethod
    def setup(cls):
        pass

    @classmethod
    def install(cls, packages: Dict[(str, List[str])]) -> bool:
        pass

    @classmethod
    def update(cls) -> bool:
        cmd_lst = ['sudo', '-E']
        cmd_lst.extend(cls.command())
        cmd_lst.extend(['update'])
        return call(cmd_lst, stdin=True) == 0

    @classmethod
    def check(cls) -> bool:
        return cls.operating_system() in {OperatingSystem.Linux} and which(cls.command()[0]) is not None