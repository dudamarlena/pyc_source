# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/models/multivariate/variable.py
# Compiled at: 2019-02-15 14:39:00
# Size of source mod 2**32: 2964 bytes
import pandas as pd
from pyFTS.common import fts, FuzzySet, FLR, Membership, tree
from pyFTS.partitioners import Grid
from pyFTS.models.multivariate import FLR as MVFLR

class Variable:
    """Variable"""

    def __init__(self, name, **kwargs):
        r"""

        :param name:
        :param \**kwargs: See below

        :Keyword Arguments:
            * *alias* -- Alternative name for the variable
        """
        self.name = name
        self.alias = kwargs.get('alias', self.name)
        self.data_label = kwargs.get('data_label', self.name)
        self.type = kwargs.get('type', 'common')
        self.data_type = kwargs.get('data_type', None)
        self.mask = kwargs.get('mask', None)
        self.transformation = kwargs.get('transformation', None)
        self.transformation_params = kwargs.get('transformation_params', None)
        self.partitioner = None
        self.alpha_cut = kwargs.get('alpha_cut', 0.0)
        if kwargs.get('data', None) is not None:
            (self.build)(**kwargs)

    def build(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        fs = kwargs.get('partitioner', Grid.GridPartitioner)
        mf = kwargs.get('func', Membership.trimf)
        np = kwargs.get('npart', 10)
        data = kwargs.get('data', None)
        kw = kwargs.get('partitioner_specific', {})
        self.partitioner = fs(data=data[self.data_label].values, npart=np, func=mf, transformation=self.transformation, 
         prefix=self.alias, variable=self.name, **kw)
        self.partitioner.name = self.name + ' ' + self.partitioner.name

    def apply_transformations(self, data, **kwargs):
        if kwargs.get('params', None) is not None:
            self.transformation_params = kwargs.get('params', None)
        if self.transformation is not None:
            return self.transformation.apply(data, self.transformation_params)
        else:
            return data

    def apply_inverse_transformations(self, data, **kwargs):
        if kwargs.get('params', None) is not None:
            self.transformation_params = kwargs.get('params', None)
        if self.transformation is not None:
            return self.transformation.inverse(data, self.transformation_params)
        else:
            return data

    def __str__(self):
        return self.name