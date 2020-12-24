# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/independence/graph/Lasso.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 3857 bytes
__doc__ = 'Build undirected graph out of raw data.\n\nAuthor: Diviyan Kalainathan\nDate: 1/06/17\n\n.. MIT License\n..\n.. Copyright (c) 2018 Diviyan Kalainathan\n..\n.. Permission is hereby granted, free of charge, to any person obtaining a copy\n.. of this software and associated documentation files (the "Software"), to deal\n.. in the Software without restriction, including without limitation the rights\n.. to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n.. copies of the Software, and to permit persons to whom the Software is\n.. furnished to do so, subject to the following conditions:\n..\n.. The above copyright notice and this permission notice shall be included in all\n.. copies or substantial portions of the Software.\n..\n.. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n.. IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n.. FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n.. AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n.. LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n.. OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n.. SOFTWARE.\n\n'
import networkx as nx
from sklearn.covariance import GraphicalLasso
from .model import GraphSkeletonModel, FeatureSelectionModel
from .HSICLasso import hsiclasso
import numpy as np

class Glasso(GraphSkeletonModel):
    """Glasso"""

    def __init__(self):
        super(Glasso, self).__init__()

    def predict(self, data, alpha=0.01, max_iter=2000, **kwargs):
        """ Predict the graph skeleton.

        Args:
            data (pandas.DataFrame): observational data
            alpha (float): regularization parameter
            max_iter (int): maximum number of iterations

        Returns:
            networkx.Graph: Graph skeleton
        """
        edge_model = GraphicalLasso(alpha=alpha, max_iter=max_iter)
        edge_model.fit(data.values)
        return nx.relabel_nodes(nx.DiGraph(edge_model.get_precision()), {idx:i for idx, i in enumerate(data.columns)})


class HSICLasso(FeatureSelectionModel):
    """HSICLasso"""

    def __init__(self):
        super(HSICLasso, self).__init__()

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
        y = np.transpose(df_target.values)
        X = np.transpose(df_features.values)
        path, beta, A, lam = hsiclasso(X, y)
        return beta