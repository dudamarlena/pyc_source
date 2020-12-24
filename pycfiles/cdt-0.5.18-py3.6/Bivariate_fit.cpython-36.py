# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/causality/pairwise/Bivariate_fit.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 3790 bytes
"""
Bivariate fit model
Author : Olivier Goudet
Date : 7/06/17

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
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.preprocessing import scale
from sklearn.metrics import mean_squared_error
import numpy as np
from .model import PairwiseModel
from sklearn.preprocessing import PolynomialFeatures
poly = PolynomialFeatures(degree=3)
from sklearn.linear_model import LinearRegression

class BivariateFit(PairwiseModel):
    __doc__ = 'Bivariate Fit model.\n\n    **Description:** The bivariate fit model is  based onon a best-fit criterion\n    relying on a Gaussian Process regressor. Used as weak baseline.\n\n    **Data Type**: Continuous\n\n    **Assumptions**: This is often a model used to show that correlation\n    :math:`\\neq` causation. It holds very weak performance, as it states that\n    the best predictive model is the causal model.\n\n    Example:\n        >>> from cdt.causality.pairwise import BivariateFit\n        >>> import networkx as nx\n        >>> import matplotlib.pyplot as plt\n        >>> from cdt.data import load_dataset\n        >>> data, labels = load_dataset(\'tuebingen\')\n        >>> obj = BivariateFit()\n        >>>\n        >>> # This example uses the predict() method\n        >>> output = obj.predict(data)\n        >>>\n        >>> # This example uses the orient_graph() method. The dataset used\n        >>> # can be loaded using the cdt.data module\n        >>> data, graph = load_dataset("sachs")\n        >>> output = obj.orient_graph(data, nx.Graph(graph))\n        >>>\n        >>> #To view the directed graph run the following command\n        >>> nx.draw_networkx(output, font_size=8)\n        >>> plt.show()\n    '

    def __init__(self, ffactor=2, maxdev=3, minc=12):
        super(BivariateFit, self).__init__()

    def predict_proba(self, dataset, **kwargs):
        """ Infer causal relationships between 2 variables using regression.

        Args:
            dataset (tuple): Couple of np.ndarray variables to classify

        Returns:
            float: Causation score (Value : 1 if a->b and -1 if b->a)
        """
        a, b = dataset
        return self.b_fit_score(b, a) - self.b_fit_score(a, b)

    def b_fit_score(self, x, y):
        """ Computes the cds statistic from variable 1 to variable 2

        Args:
            a (numpy.ndarray): Variable 1
            b (numpy.ndarray): Variable 2

        Returns:
            float: BF fit score
        """
        x = np.reshape(scale(x), (-1, 1))
        y = np.reshape(scale(y), (-1, 1))
        gp = GaussianProcessRegressor().fit(x, y)
        y_predict = gp.predict(x)
        error = mean_squared_error(y_predict, y)
        return error