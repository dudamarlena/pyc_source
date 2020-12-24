# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summerrpc/serializer.py
# Compiled at: 2018-07-31 10:42:31
"""
序列化：负责 程序中的对象 和 字节流 之间的相互转换
"""
__all__ = [
 'Serializer', 'PickleSerializer']
__authors__ = ['Tim Chow']
from abc import ABCMeta, abstractmethod
try:
    import cPickle as pickle
except ImportError:
    import pickle

import traceback
from .helper import *
from .exception import *

class Serializer(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def dumps(self, obj):
        pass

    @abstractmethod
    def loads(self, buff):
        pass

    @abstractmethod
    def get_name(self):
        pass


class PickleSerializer(Serializer, Singleton):

    def dumps(self, obj, protocol=1):
        try:
            return pickle.dumps(obj, protocol=protocol)
        except BaseException as ex:
            traceback.print_exc()
            raise SerializationError(ex)

    def loads(self, buff):
        try:
            return pickle.loads(buff)
        except BaseException as ex:
            traceback.print_exc()
            raise DeserializationError(ex)

    def get_name(self):
        return 'pickle'