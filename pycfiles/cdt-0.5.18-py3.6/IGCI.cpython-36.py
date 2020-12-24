# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/causality/pairwise/IGCI.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 5636 bytes
"""Information Geometric Causal Inference (IGCI) model.

P. Daniušis, D. Janzing, J. Mooij, J. Zscheischler, B. Steudel,
K. Zhang, B. Schölkopf:  Inferring deterministic causal relations.
Proceedings of the 26th Annual Conference on Uncertainty in Artificial  Intelligence (UAI-2010).
http://event.cwi.nl/uai2010/papers/UAI2010_0121.pdf

Adapted by Diviyan Kalainathan

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
    __doc__ = 'IGCI model.\n\n    **Description:** Information Geometric Causal Inference is a pairwise causal\n    discovery model model considering the case of minimal noise :math:`Y=f(X)`,\n    with :math:`f` invertible and leverages assymetries to predict causal\n    directions.\n\n    **Data Type:** Continuous\n\n    **Assumptions:** Only the case of invertible functions only is considered, as the\n    prediction would be trivial otherwise if the noise is minimal.\n\n    .. note::\n       P. Daniušis, D. Janzing, J. Mooij, J. Zscheischler, B. Steudel,\n       K. Zhang, B. Schölkopf:  Inferring deterministic causal relations.\n       Proceedings of the 26th Annual Conference on Uncertainty in Artificial  Intelligence (UAI-2010).\n       http://event.cwi.nl/uai2010/papers/UAI2010_0121.pdf\n\n    Example:\n        >>> from cdt.causality.pairwise import IGCI\n        >>> import networkx as nx\n        >>> import matplotlib.pyplot as plt\n        >>> from cdt.data import load_dataset\n        >>> data, labels = load_dataset(\'tuebingen\')\n        >>> obj = IGCI()\n        >>>\n        >>> # This example uses the predict() method\n        >>> output = obj.predict(data)\n        >>>\n        >>> # This example uses the orient_graph() method. The dataset used\n        >>> # can be loaded using the cdt.data module\n        >>> data, graph = load_dataset("sachs")\n        >>> output = obj.orient_graph(data, nx.Graph(graph))\n        >>>\n        >>> #To view the directed graph run the following command\n        >>> nx.draw_networkx(output, font_size=8)\n        >>> plt.show()\n    '

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