# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/skip/managers/linux_brew.py
# Compiled at: 2019-07-12 16:27:22
# Size of source mod 2**32: 398 bytes
from shutil import which
from skip.managers.brew import Brew

class LinuxBrew(Brew):

    @classmethod
    def check(cls) -> bool:
        from skip.managers.manager import OperatingSystem
        return cls.operating_system() in {OperatingSystem.Linux} and which(cls.command()[0]) is not None

    @classmethod
    def canonical_name(cls) -> str:
        return 'linux-brew'