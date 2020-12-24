# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jason/Dropbox/Ymir/WorkSpace/Code/mimircache/mimircache/profiler/abstract/abstractProfiler.py
# Compiled at: 2017-11-18 21:26:49
# Size of source mod 2**32: 584 bytes
import abc

class profilerAbstract(metaclass=abc.ABCMeta):
    __metaclass__ = abc.ABCMeta

    @abc.abstractclassmethod
    def __init__(self, cache_class, cache_size, reader):
        self.cache_class = cache_class
        self.cache_size = cache_size
        self.reader = reader
        self.num_of_trace_elements = 0

    @abc.abstractclassmethod
    def run(self):
        pass

    @abc.abstractclassmethod
    def addOneTraceElement(self, element):
        self.num_of_trace_elements += 1