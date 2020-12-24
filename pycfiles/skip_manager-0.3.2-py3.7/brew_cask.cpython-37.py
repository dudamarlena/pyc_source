# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/skip/managers/brew_cask.py
# Compiled at: 2019-07-12 16:27:22
# Size of source mod 2**32: 1371 bytes
from shutil import which
from subprocess import call
from typing import List, Dict
from skip.managers.brew import Brew

class BrewCask(Brew):

    @classmethod
    def clean(cls) -> bool:
        return Brew.clean()

    @classmethod
    def canonical_name(cls) -> str:
        return 'brew-cask'

    @classmethod
    def setup(cls) -> bool:
        pass

    @classmethod
    def install(cls, packages: Dict[(str, List[str])]) -> bool:
        print(cls.canonical_name() + ' packages: ' + str(packages))
        installed = True
        for package, flags in packages.items():
            cmd_lst = cls.command()
            cmd_lst.extend(['install', '--require-sha', package])
            cmd_lst.extend(flags)
            installed = installed and call(cmd_lst, stdin=True) == 0

        return installed

    @classmethod
    def update(cls) -> bool:
        return Brew.update()

    @classmethod
    def upgrade(cls) -> bool:
        cmd_lst = cls.command()
        cmd_lst.extend(['upgrade', '--force', '--greedy'])
        return call(cmd_lst, stdin=True) == 0

    @classmethod
    def check(cls):
        from skip.managers.manager import OperatingSystem
        return cls.operating_system() in {OperatingSystem.MacOS} and which(cls.command()[0]) is not None

    @classmethod
    def command(cls):
        return 'brew cask'.strip().split()