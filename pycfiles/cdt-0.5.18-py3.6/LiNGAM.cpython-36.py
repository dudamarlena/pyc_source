# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/causality/graph/LiNGAM.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 5581 bytes
"""LiNGAM algorithm.

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
from ...utils.R import RPackages, launch_R_script
from ...utils.Settings import SETTINGS

def message_warning(msg, *a, **kwargs):
    """Ignore everything except the message."""
    return str(msg) + '\n'


warnings.formatwarning = message_warning

class LiNGAM(GraphModel):
    __doc__ = 'LiNGAM algorithm **[R model]**.\n\n\n    **Description:** Linear Non-Gaussian Acyclic model. LiNGAM handles linear\n    structural equation models, where each variable is modeled as\n    :math:`X_j = \\sum_k \\alpha_k P_a^{k}(X_j) + E_j,  j \\in [1,d]`,\n    with  :math:`P_a^{k}(X_j)` the :math:`k`-th parent of\n    :math:`X_j` and :math:`\\alpha_k` a real scalar.\n\n    **Required R packages**: pcalg\n\n    **Data Type:** Continuous\n\n    **Assumptions:** The underlying causal model is supposed to be composed of\n    linear mechanisms and non-gaussian data. Under those assumptions, it is\n    shown that causal structure is fully identifiable (even inside the Markov\n    equivalence class).\n\n    Args:\n        verbose (bool): Sets the verbosity of the algorithm. Defaults to\n           `cdt.SETTINGS.verbose`\n\n    .. note::\n       Ref: S.  Shimizu,  P.O.  Hoyer,  A.  Hyvärinen,  A.  Kerminen  (2006)\n       A  Linear  Non-Gaussian  Acyclic Model for Causal Discovery;\n       Journal of Machine Learning Research 7, 2003–2030.\n\n    .. warning::\n       This implementation of LiNGAM does not support starting with a graph.\n\n    Example:\n        >>> import networkx as nx\n        >>> from cdt.causality.graph import LiNGAM\n        >>> from cdt.data import load_dataset\n        >>> data, graph = load_dataset("sachs")\n        >>> obj = LiNGAM()\n        >>> output = obj.predict(data)\n    '

    def __init__(self, verbose=False):
        """Init the model and its available arguments."""
        if not RPackages.pcalg:
            raise ImportError('R Package pcalg is not available.')
        super(LiNGAM, self).__init__()
        self.arguments = {'{FOLDER}':'/tmp/cdt_LiNGAM/', 
         '{FILE}':'data.csv', 
         '{VERBOSE}':'FALSE', 
         '{OUTPUT}':'result.csv'}
        self.verbose = SETTINGS.get_default(verbose=verbose)

    def orient_undirected_graph(self, data, graph):
        """Run LiNGAM on an undirected graph."""
        raise ValueError('LiNGAM cannot (yet) be ran with a skeleton/directed graph.')

    def orient_directed_graph(self, data, graph):
        """Run LiNGAM on a directed_graph."""
        raise ValueError('LiNGAM cannot (yet) be ran with a skeleton/directed graph.')

    def create_graph_from_data(self, data):
        """Run the LiNGAM algorithm.

        Args:
            data (pandas.DataFrame): DataFrame containing the data

        Returns:
            networkx.DiGraph: Prediction given by the LiNGAM algorithm.

        """
        self.arguments['{VERBOSE}'] = str(self.verbose).upper()
        results = self._run_LiNGAM(data, verbose=(self.verbose))
        return nx.relabel_nodes(nx.DiGraph(results), {idx:i for idx, i in enumerate(data.columns)})

    def _run_LiNGAM(self, data, fixedGaps=None, verbose=True):
        """Setting up and running LiNGAM with all arguments."""
        id = str(uuid.uuid4())
        os.makedirs('/tmp/cdt_LiNGAM' + id + '/')
        self.arguments['{FOLDER}'] = '/tmp/cdt_LiNGAM' + id + '/'

        def retrieve_result():
            return read_csv(('/tmp/cdt_LiNGAM' + id + '/result.csv'), delimiter=',').values

        try:
            data.to_csv(('/tmp/cdt_LiNGAM' + id + '/data.csv'), header=False, index=False)
            lingam_result = launch_R_script(('{}/R_templates/lingam.R'.format(os.path.dirname(os.path.realpath(__file__)))), (self.arguments),
              output_function=retrieve_result, verbose=verbose)
        except Exception as e:
            rmtree('/tmp/cdt_LiNGAM' + id + '')
            raise e
        except KeyboardInterrupt:
            rmtree('/tmp/cdt_LiNGAM' + id + '/')
            raise KeyboardInterrupt

        rmtree('/tmp/cdt_LiNGAM' + id + '')
        return lingam_result