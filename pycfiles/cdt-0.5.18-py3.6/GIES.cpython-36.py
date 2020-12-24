# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/causality/graph/GIES.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 7910 bytes
"""GIES algorithm.

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
import os, uuid, warnings, networkx as nx
from shutil import rmtree
from .model import GraphModel
from pandas import DataFrame, read_csv
from ...utils.R import RPackages, launch_R_script
from ...utils.Settings import SETTINGS

def message_warning(msg, *a, **kwargs):
    """Ignore everything except the message."""
    return str(msg) + '\n'


warnings.formatwarning = message_warning

class GIES(GraphModel):
    __doc__ = 'GIES algorithm **[R model]**.\n\n    **Description:** Greedy Interventional Equivalence Search algorithm.\n    A score-based Bayesian algorithm that searches heuristically the graph which minimizes\n    a likelihood score on the data. The main difference with GES is that it\n    accepts interventional data for its inference.\n\n    **Required R packages**: pcalg\n\n    **Data Type:** Continuous (``score=\'obs\'``) or Categorical (``score=\'int\'``)\n\n    **Assumptions:** The output is a Partially Directed Acyclic Graph (PDAG)\n    (A markov equivalence class). The available scores assume linearity of\n    mechanisms and gaussianity of the data.\n\n    Args:\n        score (str): Sets the score used by GIES.\n        verbose (bool): Defaults to ``cdt.SETTINGS.verbose``.\n\n    Available scores:\n        + int: GaussL0penIntScore\n        + obs: GaussL0penObsScore\n\n    .. note::\n       Ref:\n       D.M. Chickering (2002).  Optimal structure identification with greedy search.\n       Journal of Machine Learning Research 3 , 507–554\n\n       A. Hauser and P. Bühlmann (2012). Characterization and greedy learning of\n       interventional Markov equivalence classes of directed acyclic graphs.\n       Journal of Machine Learning Research 13, 2409–2464.\n\n       P. Nandy, A. Hauser and M. Maathuis (2015). Understanding consistency in\n       hybrid causal structure learning.\n       arXiv preprint 1507.02608\n\n       P. Spirtes, C.N. Glymour, and R. Scheines (2000).\n       Causation, Prediction, and Search, MIT Press, Cambridge (MA)\n\n    Example:\n        >>> import networkx as nx\n        >>> from cdt.causality.graph import GIES\n        >>> from cdt.data import load_dataset\n        >>> data, graph = load_dataset("sachs")\n        >>> obj = GIES()\n        >>> #The predict() method works without a graph, or with a\n        >>> #directed or undirected graph provided as an input\n        >>> output = obj.predict(data)    #No graph provided as an argument\n        >>>\n        >>> output = obj.predict(data, nx.Graph(graph))  #With an undirected graph\n        >>>\n        >>> output = obj.predict(data, graph)  #With a directed graph\n        >>>\n        >>> #To view the graph created, run the below commands:\n        >>> nx.draw_networkx(output, font_size=8)\n        >>> plt.show()\n    '

    def __init__(self, score='obs', verbose=False):
        """Init the model and its available arguments."""
        if not RPackages.pcalg:
            raise ImportError('R Package pcalg is not available.')
        super(GIES, self).__init__()
        self.scores = {'int':'GaussL0penIntScore',  'obs':'GaussL0penObsScore'}
        self.arguments = {'{FOLDER}':'/tmp/cdt_gies/',  '{FILE}':'data.csv', 
         '{SKELETON}':'FALSE', 
         '{GAPS}':'fixedgaps.csv', 
         '{SCORE}':'GaussL0penObsScore', 
         '{VERBOSE}':'FALSE', 
         '{OUTPUT}':'result.csv'}
        self.verbose = SETTINGS.get_default(verbose=verbose)
        self.score = score

    def orient_undirected_graph(self, data, graph):
        """Run GIES on an undirected graph.

        Args:
            data (pandas.DataFrame): DataFrame containing the data
            graph (networkx.Graph): Skeleton of the graph to orient

        Returns:
            networkx.DiGraph: Solution given by the GIES algorithm.

        """
        self.arguments['{VERBOSE}'] = str(self.verbose).upper()
        self.arguments['{SCORE}'] = self.scores[self.score]
        fe = DataFrame(nx.adj_matrix(graph, weight=None).todense())
        fg = DataFrame(1 - fe.values)
        results = self._run_gies(data, fixedGaps=fg, verbose=(self.verbose))
        return nx.relabel_nodes(nx.DiGraph(results), {idx:i for idx, i in enumerate(data.columns)})

    def orient_directed_graph(self, data, graph):
        """Run GIES on a directed_graph.

        Args:
            data (pandas.DataFrame): DataFrame containing the data
            graph (networkx.DiGraph): Skeleton of the graph to orient

        Returns:
            networkx.DiGraph: Solution given by the GIES algorithm.

        """
        warnings.warn('GIES is ran on the skeleton of the given graph.')
        return self.orient_undirected_graph(data, nx.Graph(graph))

    def create_graph_from_data(self, data):
        """Run the GIES algorithm.

        Args:
            data (pandas.DataFrame): DataFrame containing the data

        Returns:
            networkx.DiGraph: Solution given by the GIES algorithm.
        """
        self.arguments['{SCORE}'] = self.scores[self.score]
        self.arguments['{VERBOSE}'] = str(self.verbose).upper()
        results = self._run_gies(data, verbose=(self.verbose))
        return nx.relabel_nodes(nx.DiGraph(results), {idx:i for idx, i in enumerate(data.columns)})

    def _run_gies(self, data, fixedGaps=None, verbose=True):
        """Setting up and running GIES with all arguments."""
        id = str(uuid.uuid4())
        os.makedirs('/tmp/cdt_gies' + id + '/')
        self.arguments['{FOLDER}'] = '/tmp/cdt_gies' + id + '/'

        def retrieve_result():
            return read_csv(('/tmp/cdt_gies' + id + '/result.csv'), delimiter=',').values

        try:
            data.to_csv(('/tmp/cdt_gies' + id + '/data.csv'), header=False, index=False)
            if fixedGaps is not None:
                fixedGaps.to_csv(('/tmp/cdt_gies' + id + '/fixedgaps.csv'), index=False, header=False)
                self.arguments['{SKELETON}'] = 'TRUE'
            else:
                self.arguments['{SKELETON}'] = 'FALSE'
            gies_result = launch_R_script(('{}/R_templates/gies.R'.format(os.path.dirname(os.path.realpath(__file__)))), (self.arguments),
              output_function=retrieve_result, verbose=verbose)
        except Exception as e:
            rmtree('/tmp/cdt_gies' + id + '')
            raise e
        except KeyboardInterrupt:
            rmtree('/tmp/cdt_gies' + id + '/')
            raise KeyboardInterrupt

        rmtree('/tmp/cdt_gies' + id + '')
        return gies_result