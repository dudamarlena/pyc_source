# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/partitioners/Singleton.py
# Compiled at: 2019-01-28 08:22:23
# Size of source mod 2**32: 786 bytes
__doc__ = 'Even Length Grid Partitioner'
import numpy as np, math, random as rnd, functools, operator
from pyFTS.common import FuzzySet, Membership
from pyFTS.partitioners import partitioner

class SingletonPartitioner(partitioner.Partitioner):
    """SingletonPartitioner"""

    def __init__(self, **kwargs):
        (super(SingletonPartitioner, self).__init__)(name='Singleton', **kwargs)

    def build(self, data):
        sets = {}
        kwargs = {'type':self.type, 
         'variable':self.variable}
        for count, instance in enumerate(data):
            _name = self.get_name(count)
            sets[_name] = (FuzzySet.FuzzySet)(_name, (Membership.singleton), [instance], instance, **kwargs)

        return sets