# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /tmp/pip-build-n5kV9S/pyflux/pyflux/families/family.py
# Compiled at: 2018-02-01 11:59:15
import numpy as np

class Family(object):

    def __init__(self, transform=None, **kwargs):
        """
        Parameters
        ----------
        transform : str
            Whether to apply a transformation - e.g. 'exp' or 'logit'
        """
        self.transform_name = transform
        self.transform = self.transform_define(transform)
        self.itransform = self.itransform_define(transform)
        self.itransform_name = self.itransform_name_define(transform)

    @staticmethod
    def ilogit(x):
        return 1.0 / (1.0 + np.exp(-x))

    @staticmethod
    def logit(x):
        return np.log(x) - np.log(1.0 - x)

    @staticmethod
    def transform_define(transform):
        """
        This function links the user's choice of transformation with the associated numpy function
        """
        if transform == 'tanh':
            return np.tanh
        else:
            if transform == 'exp':
                return np.exp
            else:
                if transform == 'logit':
                    return Family.ilogit
                if transform is None:
                    return np.array
                return

            return

    @staticmethod
    def itransform_define(transform):
        """
        This function links the user's choice of transformation with its inverse
        """
        if transform == 'tanh':
            return np.arctanh
        else:
            if transform == 'exp':
                return np.log
            else:
                if transform == 'logit':
                    return Family.logit
                if transform is None:
                    return np.array
                return

            return

    @staticmethod
    def itransform_name_define(transform):
        """
        This function is used for model results table, displaying any transformations performed
        """
        if transform == 'tanh':
            return 'arctanh'
        else:
            if transform == 'exp':
                return 'log'
            else:
                if transform == 'logit':
                    return 'ilogit'
                if transform is None:
                    return ''
                return

            return