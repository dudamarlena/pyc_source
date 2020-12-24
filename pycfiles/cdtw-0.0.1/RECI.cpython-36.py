# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/causality/pairwise/RECI.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 4217 bytes
__doc__ = '\nBivariate fit model\nAuthor : Olivier Goudet\nDate : 7/06/17\n\n.. MIT License\n..\n.. Copyright (c) 2018 Diviyan Kalainathan\n..\n.. Permission is hereby granted, free of charge, to any person obtaining a copy\n.. of this software and associated documentation files (the "Software"), to deal\n.. in the Software without restriction, including without limitation the rights\n.. to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n.. copies of the Software, and to permit persons to whom the Software is\n.. furnished to do so, subject to the following conditions:\n..\n.. The above copyright notice and this permission notice shall be included in all\n.. copies or substantial portions of the Software.\n..\n.. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n.. IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n.. FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n.. AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n.. LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n.. OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n.. SOFTWARE.\n'
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.preprocessing import minmax_scale
from sklearn.metrics import mean_squared_error
import numpy as np
from .model import PairwiseModel
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

class RECI(PairwiseModel):
    """RECI"""

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