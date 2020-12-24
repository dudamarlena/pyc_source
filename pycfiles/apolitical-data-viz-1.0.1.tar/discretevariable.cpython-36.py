# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/apogee/models/bayes/discrete/discretevariable.py
# Compiled at: 2019-06-30 07:26:12
# Size of source mod 2**32: 1460 bytes
import numpy as np
from sklearn.preprocessing import LabelBinarizer
from apogee.factors import DiscreteFactor

class DiscreteVariable:

    def __init__(self, name: str, states: list, parameters: list=None, parents: list=None, encoders: dict=None, factor: 'DiscreteFactor'=None):
        self.name = name
        self.states = np.asarray(states, dtype=(np.str_))
        self.factor = factor
        self.parents = np.asarray((parents or []), dtype=(np.str_))
        self.parameters = parameters
        self.encoders = encoders

    def build_factor(self, network):
        variables = [
         
          self, *[network[parent] for parent in self.parents]]
        scope = np.asarray([network.id(variable) for variable in variables],
          dtype=(np.int32))
        cards = np.asarray([len(var.states) for var in variables], dtype=(np.int32))
        if self.parameters is not None:
            params = np.asarray((self.parameters), dtype=(np.float32)).flatten('F')
        else:
            params = None
        self.factor = DiscreteFactor(scope, cards, params)