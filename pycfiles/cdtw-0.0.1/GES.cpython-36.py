# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/causality/graph/GES.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 7831 bytes
__doc__ = 'GES algorithm.\n\nImported from the Pcalg package.\nAuthor: Diviyan Kalainathan\n\n.. MIT License\n..\n.. Copyright (c) 2018 Diviyan Kalainathan\n..\n.. Permission is hereby granted, free of charge, to any person obtaining a copy\n.. of this software and associated documentation files (the "Software"), to deal\n.. in the Software without restriction, including without limitation the rights\n.. to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n.. copies of the Software, and to permit persons to whom the Software is\n.. furnished to do so, subject to the following conditions:\n..\n.. The above copyright notice and this permission notice shall be included in all\n.. copies or substantial portions of the Software.\n..\n.. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n.. IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n.. FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n.. AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n.. LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n.. OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n.. SOFTWARE.\n'
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

class GES(GraphModel):
    """GES"""

    def __init__(self, score='obs', verbose=None):
        """Init the model and its available arguments."""
        if not RPackages.pcalg:
            raise ImportError('R Package pcalg is not available.')
        super(GES, self).__init__()
        self.scores = {'int':'GaussL0penIntScore',  'obs':'GaussL0penObsScore'}
        self.arguments = {'{FOLDER}':'/tmp/cdt_ges/',  '{FILE}':'data.csv', 
         '{SKELETON}':'FALSE', 
         '{GAPS}':'fixedgaps.csv', 
         '{SCORE}':'GaussL0penObsScore', 
         '{VERBOSE}':'FALSE', 
         '{OUTPUT}':'result.csv'}
        self.verbose = SETTINGS.get_default(verbose=verbose)
        self.score = score

    def orient_undirected_graph(self, data, graph):
        """Run GES on an undirected graph.

        Args:
            data (pandas.DataFrame): DataFrame containing the data
            graph (networkx.Graph): Skeleton of the graph to orient

        Returns:
            networkx.DiGraph: Solution given by the GES algorithm.

        """
        self.arguments['{VERBOSE}'] = str(self.verbose).upper()
        self.arguments['{SCORE}'] = self.scores[self.score]
        fe = DataFrame(nx.adj_matrix(graph, weight=None).todense())
        fg = DataFrame(1 - fe.values)
        results = self._run_ges(data, fixedGaps=fg, verbose=(self.verbose))
        return nx.relabel_nodes(nx.DiGraph(results), {idx:i for idx, i in enumerate(data.columns)})

    def orient_directed_graph(self, data, graph):
        """Run GES on a directed graph.

        Args:
            data (pandas.DataFrame): DataFrame containing the data
            graph (networkx.DiGraph): Skeleton of the graph to orient

        Returns:
            networkx.DiGraph: Solution given by the GES algorithm.
        """
        warnings.warn('GES is ran on the skeleton of the given graph.')
        return self.orient_undirected_graph(data, nx.Graph(graph))

    def create_graph_from_data(self, data):
        """Run the GES algorithm.

        Args:
            data (pandas.DataFrame): DataFrame containing the data

        Returns:
            networkx.DiGraph: Solution given by the GES algorithm.

        """
        self.arguments['{SCORE}'] = self.scores[self.score]
        self.arguments['{VERBOSE}'] = str(self.verbose).upper()
        results = self._run_ges(data, verbose=(self.verbose))
        return nx.relabel_nodes(nx.DiGraph(results), {idx:i for idx, i in enumerate(data.columns)})

    def _run_ges(self, data, fixedGaps=None, verbose=True):
        """Setting up and running ges with all arguments."""
        id = str(uuid.uuid4())
        os.makedirs('/tmp/cdt_ges' + id + '/')
        self.arguments['{FOLDER}'] = '/tmp/cdt_ges' + id + '/'

        def retrieve_result():
            return read_csv(('/tmp/cdt_ges' + id + '/result.csv'), delimiter=',').values

        try:
            data.to_csv(('/tmp/cdt_ges' + id + '/data.csv'), header=False, index=False)
            if fixedGaps is not None:
                fixedGaps.to_csv(('/tmp/cdt_ges' + id + '/fixedgaps.csv'), index=False, header=False)
                self.arguments['{SKELETON}'] = 'TRUE'
            else:
                self.arguments['{SKELETON}'] = 'FALSE'
            ges_result = launch_R_script(('{}/R_templates/ges.R'.format(os.path.dirname(os.path.realpath(__file__)))), (self.arguments),
              output_function=retrieve_result, verbose=verbose)
        except Exception as e:
            rmtree('/tmp/cdt_ges' + id + '')
            raise e
        except KeyboardInterrupt:
            rmtree('/tmp/cdt_ges' + id + '/')
            raise KeyboardInterrupt

        rmtree('/tmp/cdt_ges' + id + '')
        return ges_result