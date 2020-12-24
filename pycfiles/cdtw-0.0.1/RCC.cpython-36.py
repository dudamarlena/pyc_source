# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/causality/pairwise/RCC.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 6776 bytes
__doc__ = 'Randomized Causation Coefficient Model.\n\nAuthor : David Lopez-Paz\nRef : Lopez-Paz, David and Muandet, Krikamol and Schölkopf, Bernhard and Tolstikhin, Ilya O,\n     "Towards a Learning Theory of Cause-Effect Inference", ICML 2015.\n\n.. MIT License\n..\n.. Copyright (c) 2018 Diviyan Kalainathan\n..\n.. Permission is hereby granted, free of charge, to any person obtaining a copy\n.. of this software and associated documentation files (the "Software"), to deal\n.. in the Software without restriction, including without limitation the rights\n.. to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n.. copies of the Software, and to permit persons to whom the Software is\n.. furnished to do so, subject to the following conditions:\n..\n.. The above copyright notice and this permission notice shall be included in all\n.. copies or substantial portions of the Software.\n..\n.. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n.. IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n.. FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n.. AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n.. LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n.. OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n.. SOFTWARE.\n'
from sklearn.preprocessing import scale
from sklearn.ensemble import RandomForestClassifier as CLF
from ...utils.Settings import SETTINGS
import pandas, numpy as np
from .model import PairwiseModel

class RCC(PairwiseModel):
    """RCC"""

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