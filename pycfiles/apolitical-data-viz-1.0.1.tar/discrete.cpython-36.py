# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/apogee/models/variables/discrete.py
# Compiled at: 2019-06-30 10:02:18
# Size of source mod 2**32: 2814 bytes
from typing import List, Union
from numpy import ndarray, asarray, float32, zeros, int32
from sklearn.preprocessing import LabelEncoder
from apogee.models import variables
from apogee.factors import DiscreteFactor

class DiscreteVariable(variables.BaseVariable):

    def __init__(self, *args, states, parameters=None, alpha=0, **kwargs):
        """
        A utility class to wrap a DiscreteFactor with human-intelligible labels.

        Parameters
        ----------
        args
        states: list
        parameters: list
        alpha: int
        kwargs

        """
        (super().__init__)(*args, **kwargs)
        self.states = states
        self.parameters = parameters
        self.alpha = alpha

    def fit(self, x: ndarray) -> 'DiscreteVariable':
        encoded = zeros((x.shape), dtype=int32)
        for i, _ in enumerate(self.scope):
            encoded[:, i] = LabelEncoder().fit_transform(x[:, i])

        f = DiscreteFactor((self.iscope), (self.icards), alpha=(self.alpha))
        f.fit(encoded)
        self.parameters = f.parameters
        return self

    @property
    def iscope(self):
        return asarray([
         
          self.graph.index(self.name),
         *[self.graph.index(x) for x in self.neighbours or []]])

    @property
    def icards(self):
        return asarray([
         
          len(self.states),
         *[len(self.graph[x].states) for x in self.neighbours or []]])

    @property
    def factor(self):
        if self.graph is None:
            raise ValueError("Cannot compile factor object for '{0}' without a parent graph.".format(self))
        else:
            scope = asarray([
             
              self.graph.index(self.name),
             *[self.graph.index(x) for x in self.neighbours or []]])
            cards = asarray([
             
              len(self.states),
             *[len(self.graph[x].states) for x in self.neighbours or []]])
            parameters = asarray((self.parameters), dtype=float32).flatten('F') if self.parameters is not None else None
        return DiscreteFactor(scope, cards, parameters)

    def to_dict(self):
        return {self.name: {'neighbours':self.neighbours, 
                     'states':self.states, 
                     'parameters':self.parameters}}

    @property
    def flavour(self):
        return 'discrete'