# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/probabilistic/Mixture.py
# Compiled at: 2019-04-09 16:07:11
# Size of source mod 2**32: 744 bytes
import numpy as np, pandas as pd, matplotlib.pyplot as plt
from pyFTS.common import FuzzySet, SortedCollection, tree
from pyFTS.probabilistic import ProbabilityDistribution

class Mixture(ProbabilityDistribution.ProbabilityDistribution):
    """Mixture"""

    def __init__(self, type='mixture', **kwargs):
        self.models = []
        self.weights = []

    def append_model(self, model, weight):
        self.models.append(model)
        self.weights.append(weight)

    def density(self, values):
        if not isinstance(values, list):
            values = [
             values]