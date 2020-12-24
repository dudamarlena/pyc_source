# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/independence/stats/all_types.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 5117 bytes
__doc__ = 'Dependency criteria covering all types (Numerical, Categorical, Binary).\n\nAuthor: Diviyan Kalainathan\nDate: 1/06/2017\n\n.. MIT License\n..\n.. Copyright (c) 2018 Diviyan Kalainathan\n..\n.. Permission is hereby granted, free of charge, to any person obtaining a copy\n.. of this software and associated documentation files (the "Software"), to deal\n.. in the Software without restriction, including without limitation the rights\n.. to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n.. copies of the Software, and to permit persons to whom the Software is\n.. furnished to do so, subject to the following conditions:\n..\n.. The above copyright notice and this permission notice shall be included in all\n.. copies or substantial portions of the Software.\n..\n.. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n.. IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n.. FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n.. AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n.. LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n.. OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n.. SOFTWARE.\n'
import sklearn.metrics as metrics, numpy as np
from .model import IndependenceModel

def bin_variable(var, bins='fd'):
    """Bin variables w/ normalization."""
    var = np.array(var).astype(np.float)
    var = (var - np.mean(var)) / np.std(var)
    var = np.digitize(var, np.histogram(var, bins=bins)[1])
    return var


class AdjMI(IndependenceModel):
    """AdjMI"""

    def __init__(self):
        super(AdjMI, self).__init__()

    def predict(self, a, b, **kwargs):
        """Perform the independence test.

        :param a: input data
        :param b: input data
        :type a: array-like, numerical data
        :type b: array-like, numerical data
        :return: dependency statistic (1=Highly dependent, 0=Not dependent)
        :rtype: float
        """
        binning_alg = kwargs.get('bins', 'fd')
        return metrics.adjusted_mutual_info_score(bin_variable(a, bins=binning_alg), bin_variable(b, bins=binning_alg))


class NormMI(IndependenceModel):
    """NormMI"""

    def __init__(self):
        super(NormMI, self).__init__()

    def predict(self, a, b, **kwargs):
        """Perform the independence test.

        :param a: input data
        :param b: input data
        :type a: array-like, numerical data
        :type b: array-like, numerical data
        :return: dependency statistic (1=Highly dependent, 0=Not dependent)
        :rtype: float
        """
        binning_alg = kwargs.get('bins', 'fd')
        return metrics.adjusted_mutual_info_score(bin_variable(a, bins=binning_alg), bin_variable(b, bins=binning_alg))