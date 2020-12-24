# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/causality/graph/PC.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 13545 bytes
"""PC algorithm by C.Glymour & P.Sprites (REF, 2000).

Imported from the Pcalg package.
Author = Diviyan Kalainathan

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
    __doc__ = 'PC algorithm **[R model]**.\n\n    **Description:** PC (Peter - Clark) One of the most famous score based\n    approaches for causal discovery. Based on conditional tests on variables\n    and sets of variables, it proved itself to be really efficient.\n\n    **Required R packages**: pcalg, kpcalg, RCIT (variant, see notes)\n\n    **Data Type:** Continuous and discrete\n\n    **Assumptions:** This approach\'s complexity grows rapidly with the number\n    of variables, even for quick tests. Consider graphs < 200 variables.\n    The model assumptions made by this approch mainly depend on the type of\n    test used. Kernel-based tests are also available. The prediction of PC\n    is a CPDAG (identifiability up to the Markov equivalence class).\n\n    Args:\n        CItest (str): Test for conditional independence.\n        alpha (float): significance level (number in (0, 1) for the individual\n           conditional independence tests.\n        njobs (int): number of processor cores to use for parallel computation.\n           Only available for method = "stable.fast" (set as default).\n        verbose: if TRUE, detailed output is provided.\n\n    Attributes:\n        arguments (dict): contains all current parameters used in the PC\n           algorithm execution.\n        dir_CI_test (dict): contains all available conditional independence\n           tests.\n        dir_method_indep (dict): contains all available heuristics for CI\n           testing.\n\n    .. Available heuristics for conditional independence tests:\n    ..     + gaussian: "pcalg::gaussCItest"\n    ..     + hsic: "kpcalg::kernelCItest"\n    ..     + discrete: "pcalg::disCItest"\n    ..     + binary: "pcalg::binCItest"\n    ..     + randomized: "RCIT:::CItest"\n\n    .. Available CI tests:\n    ..     + dcc: "data=X, ic.method="dcc""\n    ..     + hsic_gamma: "data=X, ic.method="hsic.gamma""\n    ..     + hsic_perm: "data=X, ic.method="hsic.perm""\n    ..     + hsic_clust: "data=X, ic.method="hsic.clust""\n    ..     + corr: "C = cor(X), n = nrow(X)"\n    ..     + rcit: "data=X, ic.method="RCIT::RCIT""\n    ..     + rcot: "data=X, ic.method="RCIT::RCoT""\n\n    Available CI tests:\n        + binary: "data=X, ic.method="dcc""\n        + discrete: "data=X, ic.method="dcc""\n        + hsic_gamma: "data=X, ic.method="hsic.gamma""\n        + hsic_perm: "data=X, ic.method="hsic.perm""\n        + hsic_clust: "data=X, ic.method="hsic.clust""\n        + gaussian: "C = cor(X), n = nrow(X)"\n        + rcit: "data=X, ic.method="RCIT::RCIT""\n        + rcot: "data=X, ic.method="RCIT::RCoT""\n\n    Default Parameters:\n        + FILE: \'/tmp/cdt_pc/data.csv\'\n        + SKELETON: \'FALSE\'\n        + EDGES: \'/tmp/cdt_pc/fixededges.csv\'\n        + GAPS: \'/tmp/cdt_pc/fixedgaps.csv\'\n        + CITEST: "pcalg::gaussCItest"\n        + METHOD_INDEP: "C = cor(X), n = nrow(X)"\n        + SELMAT: \'NULL\'\n        + DIRECTED: \'TRUE\'\n        + SETOPTIONS: \'NULL\'\n        + ALPHA: \'0.01\'\n        + VERBOSE: \'FALSE\'\n        + OUTPUT: \'/tmp/cdt_pc/result.csv\'\n\n    .. note::\n       Ref:\n       D.Colombo and M.H. Maathuis (2014).\n       Order-independent constraint-based causal structure learning.\n       Journal of Machine Learning Research 15 3741-3782.\n\n       M. Kalisch, M. Maechler, D. Colombo, M.H. Maathuis and P. Buehlmann (2012).\n       Causal Inference Using Graphical Models with the R Package pcalg.\n       Journal of Statistical Software 47(11) 1–26, http://www.jstatsoft.org/v47/i11/\n\n       M. Kalisch and P. Buehlmann (2007).\n       Estimating high-dimensional directed acyclic graphs with the PC-algorithm.\n       JMLR 8 613-636.\n\n       J. Ramsey, J. Zhang and P. Spirtes (2006).\n       Adjacency-faithfulness and conservative causal inference.\n       In Proceedings of the 22nd Annual Conference on Uncertainty in Artificial\n       Intelligence. AUAI Press, Arlington, VA.\n\n       P. Spirtes, C. Glymour and R. Scheines (2000).\n       Causation, Prediction, and Search, 2nd edition. The MIT Press\n\n       Strobl, E. V., Zhang, K., & Visweswaran, S. (2017). Approximate\n       Kernel-based Conditional Independence Tests for Fast Non-Parametric\n       Causal Discovery. arXiv preprint arXiv:1702.03877.\n\n       Imported from the Pcalg package.\n\n       The RCIT package has been adapted to fit the `CDT` package, please use the variant available at\n       https://github.com/Diviyan-Kalainathan/RCIT\n\n    Example:\n        >>> import networkx as nx\n        >>> from cdt.causality.graph import PC\n        >>> from cdt.data import load_dataset\n        >>> data, graph = load_dataset("sachs")\n        >>> obj = PC()\n        >>> #The predict() method works without a graph, or with a\n        >>> #directed or undirected graph provided as an input\n        >>> output = obj.predict(data)    #No graph provided as an argument\n        >>>\n        >>> output = obj.predict(data, nx.Graph(graph))  #With an undirected graph\n        >>>\n        >>> output = obj.predict(data, graph)  #With a directed graph\n        >>>\n        >>> #To view the graph created, run the below commands:\n        >>> nx.draw_networkx(output, font_size=8)\n        >>> plt.show()\n    '

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