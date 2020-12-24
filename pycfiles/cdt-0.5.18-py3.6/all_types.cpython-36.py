# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/independence/stats/all_types.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 5117 bytes
"""Dependency criteria covering all types (Numerical, Categorical, Binary).

Author: Diviyan Kalainathan
Date: 1/06/2017

.. MIT License
..
.. Copyright (c) 2018 Diviyan Kalainathan
..
.. Permission is hereby granted, free of charge, to any person obtaining a copy
.. of this software and associated documentation files (the "Software"), to deal
.. in the Software without restriction, including without limitation the rights
.. to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
.. copies of the Software, and to permit persons to whom the Software is
.. furnished to do so, subject to the following conditions:
..
.. The above copyright notice and this permission notice shall be included in all
.. copies or substantial portions of the Software.
..
.. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
.. IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
.. FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
.. AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
.. LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
.. OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
.. SOFTWARE.
"""
import sklearn.metrics as metrics, numpy as np
from .model import IndependenceModel

def bin_variable(var, bins='fd'):
    """Bin variables w/ normalization."""
    var = np.array(var).astype(np.float)
    var = (var - np.mean(var)) / np.std(var)
    var = np.digitize(var, np.histogram(var, bins=bins)[1])
    return var


class AdjMI(IndependenceModel):
    __doc__ = 'Dependency criterion made of binning and mutual information.\n\n    The dependency metric relies on using the clustering metric adjusted mutual information applied\n    to binned variables using the Freedman Diaconis Estimator.\n\n    .. note::\n       Ref: Vinh, Nguyen Xuan and Epps, Julien and Bailey, James, "Information theoretic measures for clusterings\n       comparison: Variants, properties, normalization and correction for chance", Journal of Machine Learning\n       Research, Volume 11, Oct 2010.\n       Ref: Freedman, David and Diaconis, Persi, "On the histogram as a density estimator:L2 theory",\n       "Zeitschrift für Wahrscheinlichkeitstheorie und Verwandte Gebiete", 1981, issn=1432-2064,\n       doi=10.1007/BF01025868.\n       \n   Example:\n       >>> from cdt.independence.stats import AdjMI\n       >>> obj = AdjMI()\n       >>> a = np.array([1, 2, 1, 5])\n       >>> b = np.array([1, 3, 0, 6])\n       >>> obj.predict(a, b)\n    '

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
    __doc__ = 'Dependency criterion made of binning and mutual information.\n\n    The dependency metric relies on using the clustering metric adjusted mutual information applied\n    to binned variables using the Freedman Diaconis Estimator.\n    :param a: input data\n    :param b: input data\n    :type a: array-like, numerical data\n    :type b: array-like, numerical data\n    :return: dependency statistic (1=Highly dependent, 0=Not dependent)\n    :rtype: float\n\n    .. note::\n       Ref: Vinh, Nguyen Xuan and Epps, Julien and Bailey, James, "Information theoretic measures for clusterings\n       comparison: Variants, properties, normalization and correction for chance", Journal of Machine Learning\n       Research, Volume 11, Oct 2010.\n       Ref: Freedman, David and Diaconis, Persi, "On the histogram as a density estimator:L2 theory",\n       "Zeitschrift für Wahrscheinlichkeitstheorie und Verwandte Gebiete", 1981, issn=1432-2064,\n       doi=10.1007/BF01025868.\n       \n    Example:\n        >>> from cdt.independence.stats import NormMI\n        >>> obj = NormMI()\n        >>> a = np.array([1, 2, 1, 5])\n        >>> b = np.array([1, 3, 0, 6])\n        >>> obj.predict(a, b)\n\n    '

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