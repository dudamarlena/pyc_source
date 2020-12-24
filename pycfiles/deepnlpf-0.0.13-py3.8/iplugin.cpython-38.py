# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/deepnlpf/core/iplugin.py
# Compiled at: 2020-04-07 17:08:27
# Size of source mod 2**32: 657 bytes
from abc import abstractmethod, ABCMeta

class IPlugin(object, metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, id_pool, lang, document, pipeline, **args):
        raise NotImplementedError('subclasses must override __init__() !')

    @abstractmethod
    def run(self):
        raise NotImplementedError('subclasses must override run() !')

    @abstractmethod
    def wrapper(self):
        raise NotImplementedError('subclasses must override wrapper() !')

    @abstractmethod
    def out_format(self, annotation):
        raise NotImplementedError('subclasses must override out_format() !')