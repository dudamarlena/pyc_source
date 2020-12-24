# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/causality/pairwise/RECI.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 4217 bytes
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
from sklearn.preprocessing import minmax_scale
from sklearn.metrics import mean_squared_error
import numpy as np
from .model import PairwiseModel
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

class RECI(PairwiseModel):
    __doc__ = 'RECI model.\n\n    **Description:** Regression Error based Causal Inference (RECI)\n    relies on a best-fit mse with monome regressor and [0,1] rescaling to\n    infer causal direction.\n\n    **Data Type:** Continuous (depends on the regressor used)\n\n    **Assumptions:** No independence tests are used, but the assumptions on\n    the model depend on the regessor used for RECI.\n\n    Args:\n        degree (int): Degree of the polynomial regression.\n\n    .. note::\n       Bloebaum, P., Janzing, D., Washio, T., Shimizu, S., & Schoelkopf, B.\n       (2018, March). Cause-Effect Inference by Comparing Regression Errors.\n       In International Conference on Artificial Intelligence and Statistics (pp. 900-909).\n\n    Example:\n        >>> from cdt.causality.pairwise import RECI\n        >>> import networkx as nx\n        >>> import matplotlib.pyplot as plt\n        >>> from cdt.data import load_dataset\n        >>> data, labels = load_dataset(\'tuebingen\')\n        >>> obj = RECI()\n        >>>\n        >>> # This example uses the predict() method\n        >>> output = obj.predict(data)\n        >>>\n        >>> # This example uses the orient_graph() method. The dataset used\n        >>> # can be loaded using the cdt.data module\n        >>> data, graph = load_dataset("sachs")\n        >>> output = obj.orient_graph(data, nx.Graph(graph))\n        >>>\n        >>> #To view the directed graph run the following command\n        >>> nx.draw_networkx(output, font_size=8)\n        >>> plt.show()\n    '

    def __init__(self, degree=3):
        super(RECI, self).__init__()
        self.degree = degree

    def predict_proba(self, dataset, **kwargs):
        """ Infer causal relationships between 2 variables using the RECI statistic

        Args:
            dataset (tuple): Couple of np.ndarray variables to classify

        Returns:
            float: Causation coefficient (Value : 1 if a->b and -1 if b->a)
        """
        a, b = dataset
        return self.b_fit_score(b, a) - self.b_fit_score(a, b)

    def b_fit_score(self, x, y):
        """ Compute the RECI fit score

        Args:
            x (numpy.ndarray): Variable 1
            y (numpy.ndarray): Variable 2

        Returns:
            float: RECI fit score

        """
        x = np.reshape(minmax_scale(x), (-1, 1))
        y = np.reshape(minmax_scale(y), (-1, 1))
        poly = PolynomialFeatures(degree=(self.degree))
        poly_x = poly.fit_transform(x)
        poly_x[:, 1] = 0
        poly_x[:, 2] = 0
        regressor = LinearRegression()
        regressor.fit(poly_x, y)
        y_predict = regressor.predict(poly_x)
        error = mean_squared_error(y_predict, y)
        return error