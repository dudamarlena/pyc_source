# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/pyFTS/common/Transformations.py
# Compiled at: 2018-08-29 15:16:28
# Size of source mod 2**32: 6648 bytes
__doc__ = '\nCommon data transformation used on pre and post processing of the FTS\n'
import numpy as np, math
from pyFTS import *

class Transformation(object):
    """Transformation"""

    def __init__(self, **kwargs):
        self.is_invertible = True
        self.minimal_length = 1

    def apply(self, data, param, **kwargs):
        """
        Apply the transformation on input data

        :param data: input data
        :param param:
        :param kwargs:
        :return: numpy array with transformed data
        """
        pass

    def inverse(self, data, param, **kwargs):
        """

        :param data: transformed data
        :param param:
        :param kwargs:
        :return: numpy array with inverse transformed data
        """
        pass

    def __str__(self):
        return self.__class__.__name__ + '(' + str(self.parameters) + ')'


class Differential(Transformation):
    """Differential"""

    def __init__(self, lag):
        super(Differential, self).__init__()
        self.lag = lag
        self.minimal_length = 2

    @property
    def parameters(self):
        return self.lag

    def apply(self, data, param=None, **kwargs):
        if param is not None:
            self.lag = param
        else:
            if not isinstance(data, (list, np.ndarray, np.generic)):
                data = [
                 data]
            if isinstance(data, (np.ndarray, np.generic)):
                data = data.tolist()
        n = len(data)
        diff = [data[t] - data[(t - self.lag)] for t in np.arange(self.lag, n)]
        for t in np.arange(0, self.lag):
            diff.insert(0, 0)

        return diff

    def inverse(self, data, param, **kwargs):
        type = kwargs.get('type', 'point')
        steps_ahead = kwargs.get('steps_ahead', 1)
        if isinstance(data, (np.ndarray, np.generic)):
            data = data.tolist()
        if not isinstance(data, list):
            data = [
             data]
        n = len(data)
        if steps_ahead == 1:
            if type == 'point':
                inc = [data[t] + param[t] for t in np.arange(0, n)]
            else:
                if type == 'interval':
                    inc = [[data[t][0] + param[t], data[t][1] + param[t]] for t in np.arange(0, n)]
                elif type == 'distribution':
                    for t in np.arange(0, n):
                        data[t].differential_offset(param[t])

                    inc = data
        else:
            if type == 'point':
                inc = [
                 data[0] + param[0]]
                for t in np.arange(1, steps_ahead):
                    inc.append(data[t] + inc[(t - 1)])

            else:
                if type == 'interval':
                    inc = [
                     [
                      data[0][0] + param[0], data[0][1] + param[0]]]
                    for t in np.arange(1, steps_ahead):
                        inc.append([data[t][0] + np.nanmean(inc[(t - 1)]), data[t][1] + np.nanmean(inc[(t - 1)])])

                else:
                    if type == 'distribution':
                        data[0].differential_offset(param[0])
                        for t in np.arange(1, steps_ahead):
                            ex = data[(t - 1)].expected_value()
                            data[t].differential_offset(ex)

                        inc = data
            if n == 1:
                return inc[0]
            else:
                return inc


class Scale(Transformation):
    """Scale"""

    def __init__(self, min=0, max=1):
        super(Scale, self).__init__()
        self.data_max = None
        self.data_min = None
        self.transf_max = max
        self.transf_min = min

    @property
    def parameters(self):
        return [
         self.transf_max, self.transf_min]

    def apply(self, data, param=None, **kwargs):
        if self.data_max is None:
            self.data_max = np.nanmax(data)
            self.data_min = np.nanmin(data)
        else:
            data_range = self.data_max - self.data_min
            transf_range = self.transf_max - self.transf_min
            if isinstance(data, list):
                tmp = [(k + -1 * self.data_min) / data_range for k in data]
                tmp2 = [k * transf_range + self.transf_min for k in tmp]
            else:
                tmp = (data + -1 * self.data_min) / data_range
            tmp2 = tmp * transf_range + self.transf_min
        return tmp2

    def inverse(self, data, param, **kwargs):
        data_range = self.data_max - self.data_min
        transf_range = self.transf_max - self.transf_min
        if isinstance(data, list):
            tmp2 = [(k - self.transf_min) / transf_range for k in data]
            tmp = [k * data_range + self.data_min for k in tmp2]
        else:
            tmp2 = (data - self.transf_min) / transf_range
            tmp = tmp2 * data_range + self.data_min
        return tmp


class AdaptiveExpectation(Transformation):
    """AdaptiveExpectation"""

    def __init__(self, parameters):
        super(AdaptiveExpectation, self).__init__(parameters)
        self.h = parameters

    @property
    def parameters(self):
        return self.parameters

    def apply(self, data, param=None, **kwargs):
        return data

    def inverse(self, data, param, **kwargs):
        n = len(data)
        inc = [param[t] + self.h * (data[t] - param[t]) for t in np.arange(0, n)]
        if n == 1:
            return inc[0]
        else:
            return inc


class BoxCox(Transformation):
    """BoxCox"""

    def __init__(self, plambda):
        super(BoxCox, self).__init__()
        self.plambda = plambda

    @property
    def parameters(self):
        return self.plambda

    def apply(self, data, param=None, **kwargs):
        if self.plambda != 0:
            modified = [(dat ** self.plambda - 1) / self.plambda for dat in data]
        else:
            modified = [np.log(dat) for dat in data]
        return np.array(modified)

    def inverse(self, data, param=None, **kwargs):
        if self.plambda != 0:
            modified = [np.exp(np.log(dat * self.plambda + 1)) / self.plambda for dat in data]
        else:
            modified = [np.exp(dat) for dat in data]
        return np.array(modified)


def Z(original):
    mu = np.mean(original)
    sigma = np.std(original)
    z = [(k - mu) / sigma for k in original]
    return z


def roi(original):
    n = len(original)
    roi = []
    for t in np.arange(0, n - 1):
        roi.append((original[(t + 1)] - original[t]) / original[t])

    return roi


def smoothing(original, lags):
    pass


def aggregate(original, operation):
    pass