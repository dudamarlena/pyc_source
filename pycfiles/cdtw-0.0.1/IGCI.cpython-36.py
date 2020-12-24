# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/causality/pairwise/IGCI.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 5636 bytes
__doc__ = 'Information Geometric Causal Inference (IGCI) model.\n\nP. Daniušis, D. Janzing, J. Mooij, J. Zscheischler, B. Steudel,\nK. Zhang, B. Schölkopf:  Inferring deterministic causal relations.\nProceedings of the 26th Annual Conference on Uncertainty in Artificial  Intelligence (UAI-2010).\nhttp://event.cwi.nl/uai2010/papers/UAI2010_0121.pdf\n\nAdapted by Diviyan Kalainathan\n\n.. MIT License\n..\n.. Copyright (c) 2018 Diviyan Kalainathan\n..\n.. Permission is hereby granted, free of charge, to any person obtaining a copy\n.. of this software and associated documentation files (the "Software"), to deal\n.. in the Software without restriction, including without limitation the rights\n.. to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n.. copies of the Software, and to permit persons to whom the Software is\n.. furnished to do so, subject to the following conditions:\n..\n.. The above copyright notice and this permission notice shall be included in all\n.. copies or substantial portions of the Software.\n..\n.. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n.. IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n.. FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n.. AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n.. LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n.. OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n.. SOFTWARE.\n'
from .model import PairwiseModel
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from scipy.special import psi
import numpy as np
min_max_scale = MinMaxScaler()
standard_scale = StandardScaler()

def eval_entropy(x):
    """Evaluate the entropy of the input variable.

    :param x: input variable 1D
    :return: entropy of x
    """
    hx = 0.0
    sx = sorted(x)
    for i, j in zip(sx[:-1], sx[1:]):
        delta = j - i
        if bool(delta):
            hx += np.log(np.abs(delta))

    hx = hx / (len(x) - 1) + psi(len(x)) - psi(1)
    return hx


def integral_approx_estimator(x, y):
    """Integral approximation estimator for causal inference.

    :param x: input variable x 1D
    :param y: input variable y 1D
    :return: Return value of the IGCI model >0 if x->y otherwise if return <0
    """
    a, b = (0.0, 0.0)
    x = np.array(x)
    y = np.array(y)
    idx, idy = np.argsort(x), np.argsort(y)
    for x1, x2, y1, y2 in zip(x[[idx]][:-1], x[[idx]][1:], y[[idx]][:-1], y[[idx]][1:]):
        if x1 != x2 and y1 != y2:
            a = a + np.log(np.abs((y2 - y1) / (x2 - x1)))

    for x1, x2, y1, y2 in zip(x[[idy]][:-1], x[[idy]][1:], y[[idy]][:-1], y[[idy]][1:]):
        if x1 != x2 and y1 != y2:
            b = b + np.log(np.abs((x2 - x1) / (y2 - y1)))

    return (a - b) / len(x)


class IGCI(PairwiseModel):
    """IGCI"""

    def __init__(self):
        super(IGCI, self).__init__()

    def predict_proba(self, dataset, ref_measure='gaussian', estimator='entropy', **kwargs):
        """Evaluate a pair using the IGCI model.

        Args:
            dataset (tuple): Couple of np.ndarray variables to classify
            refMeasure (str): Scaling method (gaussian (default),
               integral or None)
            estimator (str): method used to evaluate the pairs (entropy (default)
               or integral)}

        Returns:
            float: value of the IGCI model >0 if a->b otherwise if return <0
        """
        a, b = dataset
        estimators = {'entropy':lambda x, y: eval_entropy(x) - eval_entropy(y),  'integral':integral_approx_estimator}
        ref_measures = {'gaussian':lambda x: standard_scale.fit_transform(x.reshape((-1, 1))),  'uniform':lambda x: min_max_scale.fit_transform(x.reshape((-1, 1))), 
         'None':lambda x: x}
        ref_measure = ref_measures[ref_measure]
        _estimator = estimators[estimator]
        a = ref_measure(a)
        b = ref_measure(b)
        return _estimator(a, b)