# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/causality/graph/PC.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 13545 bytes
__doc__ = 'PC algorithm by C.Glymour & P.Sprites (REF, 2000).\n\nImported from the Pcalg package.\nAuthor = Diviyan Kalainathan\n\n.. MIT License\n..\n.. Copyright (c) 2018 Diviyan Kalainathan\n..\n.. Permission is hereby granted, free of charge, to any person obtaining a copy\n.. of this software and associated documentation files (the "Software"), to deal\n.. in the Software without restriction, including without limitation the rights\n.. to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n.. copies of the Software, and to permit persons to whom the Software is\n.. furnished to do so, subject to the following conditions:\n..\n.. The above copyright notice and this permission notice shall be included in all\n.. copies or substantial portions of the Software.\n..\n.. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n.. IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n.. FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n.. AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n.. LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n.. OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n.. SOFTWARE.\n'
import os, uuid, warnings, networkx as nx
from shutil import rmtree
from tempfile import gettempdir
from .model import GraphModel
from pandas import DataFrame, read_csv
from ...utils.Settings import SETTINGS
from ...utils.R import RPackages, launch_R_script

def message_warning(msg, *a, **kwargs):
    """Ignore everything except the message."""
    return str(msg) + '\n'


warnings.formatwarning = message_warning

class PC(GraphModel):
    """PC"""

    def __init__(self, CItest='gaussian', method_indep='corr', alpha=0.01, njobs=None, verbose=None):
        """Init the model and its available arguments."""
        if not (RPackages.pcalg and RPackages.kpcalg and RPackages.RCIT):
            raise ImportError('R Package (k)pcalg/RCIT is not available. RCIT has to be installed from https://github.com/Diviyan-Kalainathan/RCIT')
        super(PC, self).__init__()
        self.dir_CI_test = {'binary':'pcalg::binCItest',  'discrete':'pcalg::disCItest', 
         'hsic_gamma':'kpcalg::kernelCItest', 
         'hsic_perm':'kpcalg::kernelCItest', 
         'hsic_clust':'kpcalg::kernelCItest', 
         'gaussian':'pcalg::gaussCItest', 
         'rcit':'RCIT:::CItest', 
         'rcot':'RCIT:::CItest'}
        self.dir_method_indep = {'binary':'dm=X, adaptDF = FALSE',  'discrete':'dm=X, adaptDF = FALSE', 
         'hsic_gamma':'data=X, ic.method="hsic.gamma"', 
         'hsic_perm':'data=X, ic.method="hsic.perm"', 
         'hsic_clust':'data=X, ic.method="hsic.clust"', 
         'gaussian':'C = cor(X), n = nrow(X)', 
         'rcit':'data=X, ic.method="RCIT::RCIT"', 
         'rcot':'data=X, ic.method="RCIT::RCoT"'}
        self.CI_test = CItest
        self.method_indep = method_indep
        self.alpha = alpha
        self.njobs = SETTINGS.get_default(njobs=njobs)
        self.verbose = SETTINGS.get_default(verbose=verbose)
        self.arguments = {'{FOLDER}':None, 
         '{FILE}':'data.csv', 
         '{SKELETON}':'FALSE', 
         '{EDGES}':'fixededges.csv', 
         '{GAPS}':'fixedgaps.csv', 
         '{CITEST}':'pcalg::gaussCItest', 
         '{METHOD_INDEP}':'C = cor(X), n = nrow(X)', 
         '{SELMAT}':'NULL', 
         '{DIRECTED}':'TRUE', 
         '{SETOPTIONS}':'NULL', 
         '{ALPHA}':'', 
         '{VERBOSE}':'FALSE', 
         '{OUTPUT}':'result.csv'}

    def orient_undirected_graph(self, data, graph, **kwargs):
        """Run PC on an undirected graph.

        Args:
            data (pandas.DataFrame): DataFrame containing the data
            graph (networkx.Graph): Skeleton of the graph to orient

        Returns:
            networkx.DiGraph: Solution given by PC on the given skeleton.
        """
        self.arguments['{CITEST}'] = self.dir_CI_test[self.CI_test]
        self.arguments['{METHOD_INDEP}'] = self.dir_method_indep[self.CI_test]
        self.arguments['{DIRECTED}'] = 'TRUE'
        self.arguments['{ALPHA}'] = str(self.alpha)
        self.arguments['{NJOBS}'] = str(self.njobs)
        self.arguments['{VERBOSE}'] = str(self.verbose).upper()
        fe = DataFrame(nx.adj_matrix(graph, weight=None).todense())
        fg = DataFrame(1 - fe.values)
        results = self._run_pc(data, fixedEdges=fe, fixedGaps=fg, verbose=(self.verbose))
        return nx.relabel_nodes(nx.DiGraph(results), {idx:i for idx, i in enumerate(data.columns)})

    def orient_directed_graph(self, data, graph, *args, **kwargs):
        """Run PC on a directed_graph (Only takes account of the skeleton of
        the graph).

        Args:
            data (pandas.DataFrame): DataFrame containing the data
            graph (networkx.DiGraph): Skeleton of the graph to orient

        Returns:
            networkx.DiGraph: Solution given by PC on the given skeleton.

        .. warning::
           The algorithm is ran on the skeleton of the given graph.

        """
        warnings.warn('PC is ran on the skeleton of the given graph.')
        return (self.orient_undirected_graph)(data, nx.Graph(graph), *args, **kwargs)

    def create_graph_from_data(self, data, **kwargs):
        """Run the PC algorithm.

        Args:
            data (pandas.DataFrame): DataFrame containing the data

        Returns:
            networkx.DiGraph: Solution given by PC on the given data.
       """
        self.arguments['{CITEST}'] = self.dir_CI_test[self.CI_test]
        self.arguments['{METHOD_INDEP}'] = self.dir_method_indep[self.CI_test]
        self.arguments['{DIRECTED}'] = 'TRUE'
        self.arguments['{ALPHA}'] = str(self.alpha)
        self.arguments['{NJOBS}'] = str(self.njobs)
        self.arguments['{VERBOSE}'] = str(self.verbose).upper()
        results = self._run_pc(data, verbose=(self.verbose))
        return nx.relabel_nodes(nx.DiGraph(results), {idx:i for idx, i in enumerate(data.columns)})

    def _run_pc(self, data, fixedEdges=None, fixedGaps=None, verbose=True):
        """Setting up and running pc with all arguments."""
        self.arguments['{FOLDER}'] = '{0!s}/cdt_pc_{1!s}/'.format(gettempdir(), uuid.uuid4())
        run_dir = self.arguments['{FOLDER}']
        os.makedirs(run_dir, exist_ok=True)

        def retrieve_result():
            return read_csv(('{}/result.csv'.format(run_dir)), delimiter=',').values

        try:
            data.to_csv(('{}/data.csv'.format(run_dir)), header=False, index=False)
            if fixedGaps is not None:
                if fixedEdges is not None:
                    fixedGaps.to_csv(('{}/fixedgaps.csv'.format(run_dir)), index=False, header=False)
                    fixedEdges.to_csv(('{}/fixededges.csv'.format(run_dir)), index=False, header=False)
                    self.arguments['{SKELETON}'] = 'TRUE'
            else:
                self.arguments['{SKELETON}'] = 'FALSE'
            pc_result = launch_R_script(('{}/R_templates/pc.R'.format(os.path.dirname(os.path.realpath(__file__)))), (self.arguments),
              output_function=retrieve_result, verbose=verbose)
        except Exception as e:
            rmtree(run_dir)
            raise e
        except KeyboardInterrupt:
            rmtree(run_dir)
            raise KeyboardInterrupt

        rmtree(run_dir)
        return pc_result