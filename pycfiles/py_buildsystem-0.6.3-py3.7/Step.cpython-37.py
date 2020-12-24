# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\py_buildsystem\Step\Step.py
# Compiled at: 2019-06-15 04:12:13
# Size of source mod 2**32: 454 bytes
from abc import abstractmethod, ABCMeta
import py_buildsystem.ConfigReader.ConfigReader as ConfigReader

class Step(ConfigReader):
    __metaclass__ = ABCMeta

    @abstractmethod
    def perform(self):
        pass

    @abstractmethod
    def get_type(self):
        pass

    def get_name(self):
        return self.step_name

    def get_exit_code(self):
        return self.exit_code