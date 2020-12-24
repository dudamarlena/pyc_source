# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/causality/graph/CCDr.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 5680 bytes
"""CCDR algorithm.

Imported from the Pcalg package.
Author: Diviyan Kalainathan

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
from pandas import read_csv
from ...utils.Settings import SETTINGS
from ...utils.R import RPackages, launch_R_script

def message_warning(msg, *a, **kwargs):
    """Ignore everything except the message."""
    return str(msg) + '\n'


warnings.formatwarning = message_warning

class CCDr(GraphModel):
    __doc__ = 'CCDr algorithm **[R model]**.\n\n    **Description:** Concave penalized Coordinate Descent with reparametrization) structure\n    learning algorithm as described in Aragam and Zhou (2015). This is a fast,\n    score based method for learning Bayesian networks that uses sparse\n    regularization and block-cyclic coordinate descent.\n\n    **Required R packages**: sparsebn\n\n    **Data Type:** Continuous\n\n    **Assumptions:** This model does not restrict or prune the search space in\n    any way, does not assume faithfulness, does not require a known variable\n    ordering, works on observational data (i.e. without experimental\n    interventions), works effectively in high dimensions, and is capable of\n    handling graphs with several thousand variables. The output of this model\n    is a DAG.\n\n    Imported from the \'sparsebn\' package.\n\n    .. warning::\n       This implementation of CCDr does not support starting with a graph.\n\n    .. note::\n       ref: Aragam, B., & Zhou, Q. (2015). Concave penalized estimation of\n       sparse Gaussian Bayesian networks. Journal of Machine Learning Research,\n       16, 2273-2328.\n\n    Example:\n        >>> import networkx as nx\n        >>> from cdt.causality.graph import CCDr\n        >>> from cdt.data import load_dataset\n        >>> data, graph = load_dataset("sachs")\n        >>> obj = CCCDr()\n        >>> output = obj.predict(data)\n    '

    def __init__(self, verbose=None):
        """Init the model and its available arguments."""
        if not RPackages.sparsebn:
            raise ImportError('R Package sparsebn is not available.')
        super(CCDr, self).__init__()
        self.arguments = {'{FOLDER}':'/tmp/cdt_CCDR/',  '{FILE}':'data.csv', 
         '{VERBOSE}':'FALSE', 
         '{OUTPUT}':'result.csv'}
        self.verbose = SETTINGS.get_default(verbose=verbose)

    def orient_undirected_graph(self, data, graph, verbose=False, **kwargs):
        """Run CCDr on an undirected graph."""
        raise ValueError('CCDR cannot (yet) be ran with a skeleton/directed graph.')

    def orient_directed_graph(self, data, graph, *args, **kwargs):
        """Run CCDR on a directed_graph."""
        raise ValueError('CCDR cannot (yet) be ran with a skeleton/directed graph.')

    def create_graph_from_data(self, data, **kwargs):
        """Apply causal discovery on observational data using CCDr.

        Args:
            data (pandas.DataFrame): DataFrame containing the data

        Returns:
            networkx.DiGraph: Solution given by the CCDR algorithm.
        """
        self.arguments['{VERBOSE}'] = str(self.verbose).upper()
        results = self._run_ccdr(data, verbose=(self.verbose))
        return nx.relabel_nodes(nx.DiGraph(results), {idx:i for idx, i in enumerate(data.columns)})

    def _run_ccdr(self, data, fixedGaps=None, verbose=True):
        """Setting up and running CCDr with all arguments."""
        id = str(uuid.uuid4())
        os.makedirs('/tmp/cdt_CCDR' + id + '/')
        self.arguments['{FOLDER}'] = '/tmp/cdt_CCDR' + id + '/'

        def retrieve_result():
            return read_csv(('/tmp/cdt_CCDR' + id + '/result.csv'), delimiter=',').values

        try:
            data.to_csv(('/tmp/cdt_CCDR' + id + '/data.csv'), header=False, index=False)
            ccdr_result = launch_R_script(('{}/R_templates/CCDr.R'.format(os.path.dirname(os.path.realpath(__file__)))), (self.arguments),
              output_function=retrieve_result, verbose=verbose)
        except Exception as e:
            rmtree('/tmp/cdt_CCDR' + id + '')
            raise e
        except KeyboardInterrupt:
            rmtree('/tmp/cdt_CCDR' + id + '/')
            raise KeyboardInterrupt

        rmtree('/tmp/cdt_CCDR' + id + '')
        return ccdr_result