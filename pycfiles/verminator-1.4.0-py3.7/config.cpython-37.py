# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/verminator/config.py
# Compiled at: 2019-10-25 02:13:05
# Size of source mod 2**32: 768 bytes
__all__ = [
 'verminator_config']
import os

class SingletonMetaClass(type):
    __doc__ = ' A metaclass that creates a Singleton base class when called. '
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = (super(SingletonMetaClass, cls).__call__)(*args, **kwargs)
        return cls._instances[cls]


class Singleton(SingletonMetaClass('SingletonMeta', (object,), {})):
    pass


class VerminatorConfig(Singleton):
    _OEM_ORIGIN = 'tdc'
    OEM_NAME = 'tdc'

    def set_oem(self, oemname):
        if oemname is not None:
            self.OEM_NAME = oemname
        else:
            if os.getenv('OEM_NAME', ''):
                self.OEM_NAME = os.getenv('OEM_NAME')


verminator_config = VerminatorConfig()