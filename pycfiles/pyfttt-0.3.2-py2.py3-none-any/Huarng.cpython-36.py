# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/partitioners/Huarng.py
# Compiled at: 2019-01-28 08:22:24
# Size of source mod 2**32: 2015 bytes
__doc__ = '\nK. H. Huarng, “Effective lengths of intervals to improve forecasting in fuzzy time series,”\nFuzzy Sets Syst., vol. 123, no. 3, pp. 387–394, Nov. 2001.\n'
import numpy as np, math, random as rnd, functools, operator
from pyFTS.common import FuzzySet, Membership, Transformations
from pyFTS.partitioners import partitioner

class HuarngPartitioner(partitioner.Partitioner):
    """HuarngPartitioner"""

    def __init__(self, **kwargs):
        (super(HuarngPartitioner, self).__init__)(name='Huarng', **kwargs)

    def build(self, data):
        diff = Transformations.Differential(1)
        data2 = diff.apply(data)
        davg = np.abs(np.mean(data2) / 2)
        if davg <= 1.0:
            base = 0.1
        else:
            if 1 < davg <= 10:
                base = 1.0
            else:
                if 10 < davg <= 100:
                    base = 10
                else:
                    base = 100
        sets = {}
        kwargs = {'type':self.type, 
         'variable':self.variable}
        dlen = self.max - self.min
        npart = math.ceil(dlen / base)
        partition = math.ceil(self.min)
        for c in range(npart):
            _name = self.get_name(c)
            if self.membership_function == Membership.trimf:
                sets[_name] = (FuzzySet.FuzzySet)(_name, (Membership.trimf), 
                 [
                  partition - base, partition, partition + base], partition, **kwargs)
            else:
                if self.membership_function == Membership.gaussmf:
                    sets[_name] = FuzzySet.FuzzySet(_name, Membership.gaussmf, [
                     partition, base / 2], partition)
                else:
                    if self.membership_function == Membership.trapmf:
                        sets[_name] = (FuzzySet.FuzzySet)(_name, (Membership.trapmf), 
                         [
                          partition - base, partition - base / 2,
                          partition + base / 2, partition + base], partition, **kwargs)
            partition += base

        return sets