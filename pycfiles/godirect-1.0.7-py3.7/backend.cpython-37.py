# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/godirect/backend.py
# Compiled at: 2018-11-09 18:34:59
# Size of source mod 2**32: 312 bytes
from abc import ABC, abstractmethod

class GoDirectBackend(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def scan(self):
        pass

    @abstractmethod
    def scan_auto(self):
        pass

    @abstractmethod
    def connect(self, device):
        pass

    @abstractmethod
    def stop(self):
        pass