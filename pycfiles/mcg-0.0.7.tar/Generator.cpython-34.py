# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jlopes/PycharmProjects/mcg/core/Generator.py
# Compiled at: 2017-01-24 01:10:58
# Size of source mod 2**32: 202 bytes
from abc import ABCMeta, abstractmethod

class Generator(metaclass=ABCMeta):

    @abstractmethod
    def generate(self):
        pass

    @abstractmethod
    def insert_into_file(self):
        pass