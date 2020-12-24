# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/independence/stats/model.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 2648 bytes
__doc__ = 'Base class for dependence models.\n\nAuthor: Diviyan Kalainathan\n\n.. MIT License\n..\n.. Copyright (c) 2018 Diviyan Kalainathan\n..\n.. Permission is hereby granted, free of charge, to any person obtaining a copy\n.. of this software and associated documentation files (the "Software"), to deal\n.. in the Software without restriction, including without limitation the rights\n.. to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n.. copies of the Software, and to permit persons to whom the Software is\n.. furnished to do so, subject to the following conditions:\n..\n.. The above copyright notice and this permission notice shall be included in all\n.. copies or substantial portions of the Software.\n..\n.. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n.. IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n.. FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n.. AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n.. LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n.. OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n.. SOFTWARE.\n'
from networkx import Graph

class IndependenceModel(object):
    """IndependenceModel"""

    def __init__(self, predictor=None):
        """Init the model."""
        super(IndependenceModel, self).__init__()
        if predictor is not None:
            self.predict = predictor

    def predict(self, a, b):
        """Compute a dependence test statistic between variables.

        Args:
            a (numpy.ndarray): First variable
            b (numpy.ndarray): Second variable

        Returns:
            float: dependence test statistic (close to 0 -> independent)
        """
        raise NotImplementedError

    def predict_undirected_graph(self, data):
        """Build a skeleton using a pairwise independence criterion.

        Args:
            data (pandas.DataFrame): Raw data table

        Returns:
            networkx.Graph: Undirected graph representing the skeleton.
        """
        graph = Graph()
        for idx_i, i in enumerate(data.columns):
            for idx_j, j in enumerate(data.columns[idx_i + 1:]):
                score = self.predict(data[i].values, data[j].values)
                if abs(score) > 0.001:
                    graph.add_edge(i, j, weight=score)

        return graph