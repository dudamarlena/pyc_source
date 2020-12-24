# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/causality/pairwise/RCC.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 6776 bytes
"""Randomized Causation Coefficient Model.

Author : David Lopez-Paz
Ref : Lopez-Paz, David and Muandet, Krikamol and Schölkopf, Bernhard and Tolstikhin, Ilya O,
     "Towards a Learning Theory of Cause-Effect Inference", ICML 2015.

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
from sklearn.preprocessing import scale
from sklearn.ensemble import RandomForestClassifier as CLF
from ...utils.Settings import SETTINGS
import pandas, numpy as np
from .model import PairwiseModel

class RCC(PairwiseModel):
    __doc__ = 'Randomized Causation Coefficient model. 2nd approach in the Fast\n    Causation challenge.\n\n    **Description:** The Randomized causation coefficient (RCC) relies on the\n    projection of the empirical distributions into a RKHS using random cosine\n    embeddings, then classfies the pairs using a random forest based on those\n    features.\n\n    **Data Type:** Continuous, Categorical, Mixed\n\n    **Assumptions:** This method needs a substantial amount of labelled causal\n    pairs to train itself. Its final performance depends on the training set\n    used.\n\n    Args:\n        rand_coeff (int): number of randomized coefficients\n        nb_estimators (int): number of estimators\n        nb_min_leaves (int): number of min samples leaves of the estimator\n        max_depth (): (optional) max depth of the model\n        s (float): scaling\n        njobs (int): number of jobs to be run on parallel (defaults to ``cdt.SETTINGS.NJOBS``)\n        verbose (bool): verbosity (defaults to ``cdt.SETTINGS.verbose``)\n\n    .. note::\n       Ref : Lopez-Paz, David and Muandet, Krikamol and Schölkopf, Bernhard and Tolstikhin, Ilya O,\n       "Towards a Learning Theory of Cause-Effect Inference", ICML 2015.\n\n    Example:\n        >>> from cdt.causality.pairwise import RCC\n        >>> import networkx as nx\n        >>> import matplotlib.pyplot as plt\n        >>> from cdt.data import load_dataset\n        >>> from sklearn.model_selection import train_test_split\n        >>> data, labels = load_dataset(\'tuebingen\')\n        >>> X_tr, X_te, y_tr, y_te = train_test_split(data, labels, train_size=.5)\n        >>>\n        >>> obj = RCC()\n        >>> obj.fit(X_tr, y_tr)\n        >>> # This example uses the predict() method\n        >>> output = obj.predict(X_te)\n        >>>\n        >>> # This example uses the orient_graph() method. The dataset used\n        >>> # can be loaded using the cdt.data module\n        >>> data, graph = load_dataset(\'sachs\')\n        >>> output = obj.orient_graph(data, nx.DiGraph(graph))\n        >>>\n        >>> # To view the directed graph run the following command\n        >>> nx.draw_networkx(output, font_size=8)\n        >>> plt.show()\n    '

    def __init__(self, rand_coeff=333, nb_estimators=500, nb_min_leaves=20, max_depth=None, s=10, njobs=None, verbose=None):
        """Initialize the model w/ its parameters.
        """
        np.random.seed(0)
        self.K = rand_coeff
        self.E = nb_estimators
        self.L = nb_min_leaves
        self.njobs, self.verbose = SETTINGS.get_default(('njobs', njobs), ('verbose', verbose))
        self.max_depth = max_depth
        self.W = np.hstack((s * np.random.randn(self.K, 2),
         2 * np.pi * np.random.rand(self.K, 1)))
        self.W2 = np.hstack((s * np.random.randn(self.K, 1),
         2 * np.pi * np.random.rand(self.K, 1)))
        self.clf = None

    def featurize_row(self, x, y):
        """ Projects the causal pair to the RKHS using the sampled kernel approximation.

        Args:
            x (np.ndarray): Variable 1
            y (np.ndarray): Variable 2

        Returns:
            np.ndarray: projected empirical distributions into a single fixed-size vector.
        """
        x = x.ravel()
        y = y.ravel()
        b = np.ones(x.shape)
        dx = np.cos(np.dot(self.W2, np.vstack((x, b)))).mean(1)
        dy = np.cos(np.dot(self.W2, np.vstack((y, b)))).mean(1)
        if sum(dx) > sum(dy):
            return np.hstack((dx, dy,
             np.cos(np.dot(self.W, np.vstack((x, y, b)))).mean(1)))
        else:
            return np.hstack((dx, dy,
             np.cos(np.dot(self.W, np.vstack((y, x, b)))).mean(1)))

    def fit(self, x, y):
        """Train the model.

        Args:
            x_tr (pd.DataFrame): CEPC format dataframe containing the pairs
            y_tr (pd.DataFrame or np.ndarray): labels associated to the pairs
        """
        train = np.vstack((
         np.array([self.featurize_row(row.iloc[0], row.iloc[1]) for idx, row in x.iterrows()]),
         np.array([self.featurize_row(row.iloc[1], row.iloc[0]) for idx, row in x.iterrows()])))
        labels = np.vstack((y, -y)).ravel()
        verbose = 1 if self.verbose else 0
        self.clf = CLF(verbose=verbose, min_samples_leaf=(self.L),
          n_estimators=(self.E),
          max_depth=(self.max_depth),
          n_jobs=(self.njobs)).fit(train, labels)

    def predict_proba(self, dataset, **kwargs):
        """ Predict the causal score using a trained RCC model

        Args:
            dataset (tuple): Couple of np.ndarray variables to classify

        Returns:
            float: Causation score (Value : 1 if a->b and -1 if b->a)
        """
        if self.clf is None:
            raise ValueError('Model has to be trained before making predictions.')
        x, y = dataset
        input_ = self.featurize_row(x, y).reshape((1, -1))
        return self.clf.predict(input_)