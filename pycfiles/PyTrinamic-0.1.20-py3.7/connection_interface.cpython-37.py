# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\PyTrinamic\connections\connection_interface.py
# Compiled at: 2019-09-16 10:04:04
# Size of source mod 2**32: 167 bytes
"""
Created on 22.02.2019

@author: ed
"""
import abc

class connection_interface(abc.ABC):

    @abc.abstractmethod
    def printInfo(self):
        pass