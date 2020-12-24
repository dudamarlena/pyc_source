# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dora/interface/Interfaces.py
# Compiled at: 2020-01-16 10:25:08
# Size of source mod 2**32: 605 bytes
from enum import Enum

class Interfaces(Enum):
    GENERIC = 0
    ZEPPELIN = 1
    JUPYTER = 2


class Interface:

    @staticmethod
    def get_interface(interface, *args, **kargs):
        if interface is Interfaces.ZEPPELIN:
            from .zeppelin import Zeppelin
            return Zeppelin(*args, **kargs)
        if interface is Interfaces.JUPYTER:
            from .jupyter import Jupyter
            return Jupyter(*args, **kargs)
        from .generic import Generic
        return Generic(*args, **kargs)

    def get_interfaces(self):
        return Interfaces