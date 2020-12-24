# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/DBApps/Writers/listwriter.py
# Compiled at: 2019-04-22 11:39:38
# Size of source mod 2**32: 675 bytes
"""
Created on Mar 6, 2018

@author: jsk
"""
from abc import ABCMeta, abstractmethod

class ListWriter(metaclass=ABCMeta):
    __doc__ = '\n    Base class for writing lists\n    \n    :summary: holds opaque object defining the configuration.\n    subclass dependent\n    '

    @property
    def oConfig(self):
        return self._config

    @oConfig.setter
    def oConfig(self, value):
        self._config = value

    def __init__(self, configInfo):
        self._config = configInfo

    @abstractmethod
    def write_list(self, outData):
        pass