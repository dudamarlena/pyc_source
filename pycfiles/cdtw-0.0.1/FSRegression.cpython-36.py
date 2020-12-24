# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/independence/graph/FSRegression.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 8113 bytes
__doc__ = 'Methods using standard feature selection algorithms to recover the undirected graph.\n\nUsing the sklearn tools\nAuthor: Olivier Goudet\n\n.. MIT License\n..\n.. Copyright (c) 2018 Diviyan Kalainathan\n..\n.. Permission is hereby granted, free of charge, to any person obtaining a copy\n.. of this software and associated documentation files (the "Software"), to deal\n.. in the Software without restriction, including without limitation the rights\n.. to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n.. copies of the Software, and to permit persons to whom the Software is\n.. furnished to do so, subject to the following conditions:\n..\n.. The above copyright notice and this permission notice shall be included in all\n.. copies or substantial portions of the Software.\n..\n.. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n.. IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n.. FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n.. AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n.. LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n.. OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n.. SOFTWARE.\n'
from .model import FeatureSelectionModel
from sklearn.feature_selection import RFECV
from sklearn.svm import SVR, LinearSVR
from sklearn.tree import DecisionTreeRegressor
from skrebate import ReliefF
import numpy as np
from sklearn.linear_model import ARDRegression as ard

class RFECVLinearSVR(FeatureSelectionModel):
    """RFECVLinearSVR"""

    def __init__(self):
        super(RFECVLinearSVR, self).__init__()

    def predict_features(self, df_features, df_target, idx=0, **kwargs):
        """For one variable, predict its neighbouring nodes.

        Args:
            df_features (pandas.DataFrame):
            df_target (pandas.Series):
            idx (int): (optional) for printing purposes
            kwargs (dict): additional options for algorithms

        Returns:
            list: scores of each feature relatively to the target
        """
        estimator = SVR(kernel='linear')
        selector = RFECV(estimator, step=1)
        selector = selector.fit(df_features.values, np.ravel(df_target.values))
        return selector.grid_scores_


class LinearSVRL2(FeatureSelectionModel):
    """LinearSVRL2"""

    def __init__(self):
        super(LinearSVRL2, self).__init__()

    def predict_features(self, df_features, df_target, idx=0, C=0.1, **kwargs):
        """For one variable, predict its neighbouring nodes.

        Args:
            df_features (pandas.DataFrame):
            df_target (pandas.Series):
            idx (int): (optional) for printing purposes
            kwargs (dict): additional options for algorithms
            C (float): Penalty parameter of the error term

        Returns:
            list: scores of each feature relatively to the target
        """
        lsvc = LinearSVR(C=C).fit(df_features.values, np.ravel(df_target.values))
        return np.abs(lsvc.coef_)


class DecisionTreeRegression(FeatureSelectionModel):
    """DecisionTreeRegression"""

    def __init__(self):
        super(DecisionTreeRegression, self).__init__()

    def predict_features(self, df_features, df_target, idx=0, **kwargs):
        """For one variable, predict its neighbouring nodes.

        Args:
            df_features (pandas.DataFrame):
            df_target (pandas.Series):
            idx (int): (optional) for printing purposes
            kwargs (dict): additional options for algorithms

        Returns:
            list: scores of each feature relatively to the target
        """
        X = df_features.values
        y = df_target.values
        regressor = DecisionTreeRegressor()
        regressor.fit(X, y)
        return regressor.feature_importances_


class ARD(FeatureSelectionModel):
    """ARD"""

    def __init__(self):
        super(ARD, self).__init__()

    def predict_features(self, df_features, df_target, idx=0, **kwargs):
        """For one variable, predict its neighbouring nodes.

        Args:
            df_features (pandas.DataFrame):
            df_target (pandas.Series):
            idx (int): (optional) for printing purposes
            kwargs (dict): additional options for algorithms

        Returns:
            list: scores of each feature relatively to the target
        """
        X = df_features.values
        y = df_target.values
        clf = ard(compute_score=True)
        clf.fit(X, y.ravel())
        return np.abs(clf.coef_)


class RRelief(FeatureSelectionModel):
    """RRelief"""

    def __init__(self):
        super(RRelief, self).__init__()

    def predict_features(self, df_features, df_target, idx=0, **kwargs):
        """For one variable, predict its neighbouring nodes.

        Args:
            df_features (pandas.DataFrame):
            df_target (pandas.Series):
            idx (int): (optional) for printing purposes
            kwargs (dict): additional options for algorithms

        Returns:
            list: scores of each feature relatively to the target
        """
        X = df_features.values
        y = np.ravel(df_target.values)
        rr = ReliefF()
        rr.fit(X, y)
        return rr.feature_importances_