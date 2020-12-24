# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deepnlpf/iplugindb.py
# Compiled at: 2020-04-16 00:40:25
# Size of source mod 2**32: 1205 bytes
from abc import abstractmethod, ABCMeta

class IPluginDB(object, metaclass=ABCMeta):

    @abstractmethod
    def __init__(self):
        raise NotImplementedError('subclasses must override __init__(self) !')

    @abstractmethod
    def insert(self, collection, document):
        raise NotImplementedError('subclasses must override insert(self, collection, document)')

    @abstractmethod
    def select_one(self, collection, key):
        raise NotImplementedError('subclasses must override select_one(self, collection, key)')

    @abstractmethod
    def select_all(self, collection):
        raise NotImplementedError('subclasses must override out_format() !')

    @abstractmethod
    def select_all_key(self, collection, key):
        raise NotImplementedError('subclasses must override select_all_key(self, collection, key)')

    @abstractmethod
    def update(self, collection, key, document):
        raise NotImplementedError('subclasses must override update(self, collection, key, document)')

    @abstractmethod
    def delete(self, collection, key):
        raise NotImplementedError('subclasses must override delete(self, collection, key)')