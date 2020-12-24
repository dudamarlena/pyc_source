# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/skip/managers/manager.py
# Compiled at: 2019-07-12 16:27:22
# Size of source mod 2**32: 1364 bytes
from abc import ABC, abstractmethod
from enum import Enum
from typing import Dict, List

class OperatingSystem(Enum):
    Linux = 'Linux'
    Windows = 'Windows'
    MacOS = 'Darwin'


class PackageManager(ABC):

    @classmethod
    def operating_system(cls) -> OperatingSystem:
        import platform
        if platform.system() == 'Linux':
            return OperatingSystem.Linux
        if platform.system() == 'Windows':
            return OperatingSystem.Windows
        if platform.system() == 'Darwin':
            return OperatingSystem.MacOS

    @classmethod
    @abstractmethod
    def command(cls) -> List[str]:
        pass

    @classmethod
    @abstractmethod
    def canonical_name(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def setup(cls) -> bool:
        pass

    @classmethod
    @abstractmethod
    def install(cls, packages: Dict[(str, List[str])]) -> bool:
        pass

    @classmethod
    @abstractmethod
    def update(cls) -> bool:
        pass

    @classmethod
    @abstractmethod
    def upgrade(cls) -> bool:
        pass

    @classmethod
    @abstractmethod
    def remove(cls, packages: Dict[(str, List[str])]) -> bool:
        pass

    @classmethod
    @abstractmethod
    def check(cls) -> bool:
        return False

    @classmethod
    @abstractmethod
    def clean(cls) -> bool:
        pass