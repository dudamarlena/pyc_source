# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/causality/graph/bnlearn.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 21227 bytes
__doc__ = 'BN learn algorithms.\n\nImported from the bnlearn package.\nAuthor: Diviyan Kalainathan\n\n.. MIT License\n..\n.. Copyright (c) 2018 Diviyan Kalainathan\n..\n.. Permission is hereby granted, free of charge, to any person obtaining a copy\n.. of this software and associated documentation files (the "Software"), to deal\n.. in the Software without restriction, including without limitation the rights\n.. to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n.. copies of the Software, and to permit persons to whom the Software is\n.. furnished to do so, subject to the following conditions:\n..\n.. The above copyright notice and this permission notice shall be included in all\n.. copies or substantial portions of the Software.\n..\n.. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n.. IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n.. FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n.. AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n.. LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n.. OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n.. SOFTWARE.\n'
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

class BNlearnAlgorithm(GraphModel):
    """BNlearnAlgorithm"""

    def __init__(self, score='NULL', alpha=0.05, beta='NULL', optim=False, verbose=None):
        """Init the model."""
        if not RPackages.bnlearn:
            raise ImportError('R Package bnlearn is not available.')
        super(BNlearnAlgorithm, self).__init__()
        self.arguments = {'{FOLDER}':'/tmp/cdt_bnlearn/',  '{FILE}':'data.csv', 
         '{SKELETON}':'FALSE', 
         '{ALGORITHM}':None, 
         '{WHITELIST}':'whitelist.csv', 
         '{BLACKLIST}':'blacklist.csv', 
         '{SCORE}':'NULL', 
         '{OPTIM}':'FALSE', 
         '{ALPHA}':'0.05', 
         '{BETA}':'NULL', 
         '{VERBOSE}':'FALSE', 
         '{OUTPUT}':'result.csv'}
        self.score = score
        self.alpha = alpha
        self.beta = beta
        self.optim = optim
        self.verbose = SETTINGS.get_default(verbose=verbose)

    def orient_undirected_graph(self, data, graph):
        """Run the algorithm on an undirected graph.

        Args:
            data (pandas.DataFrame): DataFrame containing the data
            graph (networkx.Graph): Skeleton of the graph to orient

        Returns:
            networkx.DiGraph: Solution on the given skeleton.

        """
        self.arguments['{VERBOSE}'] = str(self.verbose).upper()
        self.arguments['{SCORE}'] = self.score
        self.arguments['{BETA}'] = str(self.beta)
        self.arguments['{OPTIM}'] = str(self.optim).upper()
        self.arguments['{ALPHA}'] = str(self.alpha)
        cols = list(data.columns)
        data.columns = [i for i in range(data.shape[1])]
        graph2 = nx.relabel_nodes(graph, {j:i for i, j in zip(['X' + str(i) for i in range(data.shape[1])], cols)})
        whitelist = DataFrame((list(nx.edges(graph2))), columns=['from', 'to'])
        blacklist = DataFrame((list(nx.edges(nx.DiGraph(DataFrame((-nx.adj_matrix(graph2, weight=None).todense() + 1), columns=(list(graph2.nodes())),
          index=(list(graph2.nodes()))))))),
          columns=['from', 'to'])
        results = self._run_bnlearn(data, whitelist=whitelist, blacklist=blacklist,
          verbose=(self.verbose))
        try:
            return nx.relabel_nodes(nx.DiGraph(results), {idx:i for idx, i in enumerate(cols)})
        except nx.exception.NetworkXError as e:
            if results.shape[1] == 2:
                output = nx.DiGraph()
                output.add_nodes_from(['X' + str(i) for i in range(data.shape[1])])
                output.add_edges_from(results)
                return nx.relabel_nodes(output, {i:j for i, j in zip(['X' + str(i) for i in range(data.shape[1])], cols)})
            raise e

    def orient_directed_graph(self, data, graph):
        """Run the algorithm on a directed_graph.

        Args:
            data (pandas.DataFrame): DataFrame containing the data
            graph (networkx.DiGraph): Skeleton of the graph to orient

        Returns:
            networkx.DiGraph: Solution on the given skeleton.

        .. warning::
           The algorithm is ran on the skeleton of the given graph.

        """
        warnings.warn('The algorithm is ran on the skeleton of the given graph.')
        return self.orient_undirected_graph(data, nx.Graph(graph))

    def create_graph_from_data(self, data):
        """Run the algorithm on data.

        Args:
            data (pandas.DataFrame): DataFrame containing the data

        Returns:
            networkx.DiGraph: Solution given by the algorithm.

        """
        self.arguments['{SCORE}'] = self.score
        self.arguments['{VERBOSE}'] = str(self.verbose).upper()
        self.arguments['{BETA}'] = str(self.beta)
        self.arguments['{OPTIM}'] = str(self.optim).upper()
        self.arguments['{ALPHA}'] = str(self.alpha)
        cols = list(data.columns)
        data.columns = [i for i in range(data.shape[1])]
        results = self._run_bnlearn(data, verbose=(self.verbose))
        graph = nx.DiGraph()
        graph.add_nodes_from(['X' + str(i) for i in range(data.shape[1])])
        graph.add_edges_from(results)
        return nx.relabel_nodes(graph, {i:j for i, j in zip(['X' + str(i) for i in range(data.shape[1])], cols)})

    def _run_bnlearn(self, data, whitelist=None, blacklist=None, verbose=True):
        """Setting up and running bnlearn with all arguments."""
        id = str(uuid.uuid4())
        os.makedirs('/tmp/cdt_bnlearn' + id + '/')
        self.arguments['{FOLDER}'] = '/tmp/cdt_bnlearn' + id + '/'

        def retrieve_result():
            return read_csv(('/tmp/cdt_bnlearn' + id + '/result.csv'), delimiter=',').values

        try:
            data.to_csv(('/tmp/cdt_bnlearn' + id + '/data.csv'), index=False)
            if blacklist is not None:
                whitelist.to_csv(('/tmp/cdt_bnlearn' + id + '/whitelist.csv'), index=False, header=False)
                blacklist.to_csv(('/tmp/cdt_bnlearn' + id + '/blacklist.csv'), index=False, header=False)
                self.arguments['{SKELETON}'] = 'TRUE'
            else:
                self.arguments['{SKELETON}'] = 'FALSE'
            bnlearn_result = launch_R_script(('{}/R_templates/bnlearn.R'.format(os.path.dirname(os.path.realpath(__file__)))), (self.arguments),
              output_function=retrieve_result, verbose=verbose)
        except Exception as e:
            rmtree('/tmp/cdt_bnlearn' + id + '')
            raise e
        except KeyboardInterrupt:
            rmtree('/tmp/cdt_bnlearn' + id + '/')
            raise KeyboardInterrupt

        rmtree('/tmp/cdt_bnlearn' + id)
        return bnlearn_result


class GS(BNlearnAlgorithm):
    """GS"""

    def __init__(self):
        super(GS, self).__init__()
        self.arguments['{ALGORITHM}'] = 'gs'


class IAMB(BNlearnAlgorithm):
    """IAMB"""

    def __init__(self):
        super(IAMB, self).__init__()
        self.arguments['{ALGORITHM}'] = 'iamb'


class Fast_IAMB(BNlearnAlgorithm):
    """Fast_IAMB"""

    def __init__(self):
        super(Fast_IAMB, self).__init__()
        self.arguments['{ALGORITHM}'] = 'fast.iamb'


class Inter_IAMB(BNlearnAlgorithm):
    """Inter_IAMB"""

    def __init__(self):
        super(Inter_IAMB, self).__init__()
        self.arguments['{ALGORITHM}'] = 'inter.iamb'


class MMPC(BNlearnAlgorithm):
    """MMPC"""

    def __init__(self):
        super(MMPC, self).__init__()
        self.arguments['{ALGORITHM}'] = 'mmpc'