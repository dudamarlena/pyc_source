# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/causality/graph/bnlearn.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 21227 bytes
"""BN learn algorithms.

Imported from the bnlearn package.
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
from pandas import DataFrame, read_csv
from ...utils.R import RPackages, launch_R_script
from ...utils.Settings import SETTINGS

def message_warning(msg, *a, **kwargs):
    """Ignore everything except the message."""
    return str(msg) + '\n'


warnings.formatwarning = message_warning

class BNlearnAlgorithm(GraphModel):
    __doc__ = "BNlearn algorithm. All these models imported from bnlearn revolve around\n    this base class and have all the same attributes/interface.\n\n    Args:\n        score (str):the label of the conditional independence test to be used in the\n           algorithm. If none is specified, the default test statistic is the mutual information\n           for categorical variables, the Jonckheere-Terpstra test for ordered factors and the\n           linear correlation for continuous variables. See below for available tests.\n        alpha (float): a numeric value, the target nominal type I error rate.\n        beta (int): a positive integer, the number of permutations considered for each permutation\n           test. It will be ignored with a warning if the conditional independence test specified by the\n           score argument is not a permutation test.\n        optim (bool): See bnlearn-package for details.\n        verbose (bool): Sets the verbosity. Defaults to SETTINGS.verbose\n\n    .. _bnlearntests:\n\n    Available tests:\n        • discrete case (categorical variables)\n           – mutual information: an information-theoretic distance measure.\n               It's proportional to the log-likelihood ratio (they differ by a 2n factor)\n               and is related to the deviance of the tested models. The asymptotic χ2 test\n               (mi and mi-adf,  with  adjusted  degrees  of  freedom), the Monte Carlo\n               permutation test (mc-mi), the sequential Monte Carlo permutation\n               test (smc-mi), and the semiparametric test (sp-mi) are implemented.\n           – shrinkage estimator for the mutual information (mi-sh)\n               An improved\n               asymptotic χ2 test based on the James-Stein estimator for the mutual\n               information.\n           – Pearson’s X2 : the classical Pearson's X2 test for contingency tables.\n               The asymptotic χ2 test (x2 and x2-adf, with adjusted degrees of freedom),\n               the Monte Carlo permutation test (mc-x2), the sequential Monte Carlo\n               permutation test (smc-x2) and semiparametric test (sp-x2) are implemented  .\n\n        • discrete case (ordered factors)\n           – Jonckheere-Terpstra : a trend test for ordinal variables.\n              The\n              asymptotic normal test (jt), the Monte Carlo permutation test (mc-jt)\n              and the sequential Monte Carlo permutation test (smc-jt) are implemented.\n\n        • continuous case (normal variables)\n           – linear  correlation:  Pearson’s  linear  correlation.\n               The exact\n               Student’s  t  test  (cor),  the Monte Carlo permutation test (mc-cor)\n               and the sequential Monte Carlo permutation test (smc-cor) are implemented.\n           – Fisher’s Z: a transformation of the linear correlation with asymptotic normal distribution.\n               Used by commercial software (such as TETRAD II)\n               for the PC algorithm (an R implementation is present in the pcalg\n               package on CRAN). The asymptotic normal test (zf), the Monte Carlo\n               permutation test (mc-zf) and the sequential Monte Carlo permutation\n               test (smc-zf) are implemented.\n           – mutual information: an information-theoretic distance measure.\n               Again\n               it is proportional to the log-likelihood ratio (they differ by a 2n\n               factor). The asymptotic χ2 test (mi-g), the Monte Carlo permutation\n               test (mc-mi-g) and the sequential Monte Carlo permutation test\n               (smc-mi-g) are implemented.\n\n           – shrinkage estimator for the mutual information(mi-g-sh):\n               an improved\n               asymptotic χ2 test based on the James-Stein estimator for the mutual\n               information.\n\n        • hybrid case (mixed discrete and normal variables)\n           – mutual information: an information-theoretic distance measure.\n               Again\n               it is proportional to the log-likelihood ratio (they differ by a 2n\n               factor). Only the asymptotic χ2 test (mi-cg) is implemented.\n    "

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
    __doc__ = 'Grow-Shrink algorithm.\n\n    **Description:** The Grow Shrink algorithm is a constraint based algorithm\n    to recover bayesian networks. It consists in two phases, one growing phase\n    in which nodes are added to the markov blanket based on conditional\n    independence and a shrinking phase in which most irrelevant nodes are\n    removed.\n\n    **Required R packages**: bnlearn\n\n    **Data Type:** Depends on the test used. Check\n    :ref:`here <bnlearntests>` for the list of available tests.\n\n    **Assumptions:** GS outputs a CPDAG, with additional assumptions depending\n    on the conditional test used.\n\n    .. note::\n       Margaritis D (2003).\n       Learning Bayesian Network Model Structure from Data\n       . Ph.D. thesis, School\n       of Computer Science, Carnegie-Mellon University, Pittsburgh, PA. Available as Technical Report\n       CMU-CS-03-153\n\n    Example:\n        >>> import networkx as nx\n        >>> from cdt.causality.graph import GS\n        >>> from cdt.data import load_dataset\n        >>> data, graph = load_dataset("sachs")\n        >>> obj = GS()\n        >>> #The predict() method works without a graph, or with a\n        >>> #directed or undirected graph provided as an input\n        >>> output = obj.predict(data)    #No graph provided as an argument\n        >>>\n        >>> output = obj.predict(data, nx.Graph(graph))  #With an undirected graph\n        >>>\n        >>> output = obj.predict(data, graph)  #With a directed graph\n        >>>\n        >>> #To view the graph created, run the below commands:\n        >>> nx.draw_networkx(output, font_size=8)\n        >>> plt.show()\n    '

    def __init__(self):
        super(GS, self).__init__()
        self.arguments['{ALGORITHM}'] = 'gs'


class IAMB(BNlearnAlgorithm):
    __doc__ = 'IAMB algorithm.\n\n    **Description:** The is a bayesian constraint based algorithm\n    to recover Markov blankets in a forward selection and a modified backward\n    selection process.\n\n    **Required R packages**: bnlearn\n\n    **Data Type:** Depends on the test used. Check\n    :ref:`here <bnlearntests>` for the list of available tests.\n\n    **Assumptions:** IAMB outputs Markov blankets of nodes,\n    with additional assumptions depending on the conditional test used.\n\n    .. note::\n       Tsamardinos  I,  Aliferis  CF,  Statnikov  A  (2003).   "Algorithms  for  Large  Scale  Markov  Blanket\n       Discovery".  In "Proceedings of the Sixteenth International Florida Artificial Intelligence Research\n       Society Conference", pp. 376-381. AAAI Press.\n\n    Example:\n        >>> import networkx as nx\n        >>> from cdt.causality.graph import IAMB\n        >>> from cdt.data import load_dataset\n        >>> data, graph = load_dataset("sachs")\n        >>> obj = IAMB()\n        >>> #The predict() method works without a graph, or with a\n        >>> #directed or undirected graph provided as an input\n        >>> output = obj.predict(data)    #No graph provided as an argument\n        >>>\n        >>> output = obj.predict(data, nx.Graph(graph))  #With an undirected graph\n        >>>\n        >>> output = obj.predict(data, graph)  #With a directed graph\n        >>>\n        >>> #To view the graph created, run the below commands:\n        >>> nx.draw_networkx(output, font_size=8)\n        >>> plt.show()\n    '

    def __init__(self):
        super(IAMB, self).__init__()
        self.arguments['{ALGORITHM}'] = 'iamb'


class Fast_IAMB(BNlearnAlgorithm):
    __doc__ = 'Fast IAMB algorithm.\n\n    **Description:** Similar to IAMB, Fast-IAMB adds speculation to provide more\n    computational performance without affecting the accuracy of markov blanket\n    recovery.\n\n    **Required R packages**: bnlearn\n\n    **Data Type:** Depends on the test used. Check\n    :ref:`here <bnlearntests>` for the list of available tests.\n\n    **Assumptions:** Fast-IAMB outputs markov blankets of nodes, with additional\n    assumptions depending on the conditional test used.\n\n    .. note::\n        Yaramakala S, Margaritis D (2005).  "Speculative Markov Blanket Discovery for Optimal Feature\n        Selection".  In "ICDM ’05:  Proceedings of the Fifth IEEE International Conference on Data\n        Mining", pp. 809-812. IEEE Computer Society.\n\n    Example:\n        >>> import networkx as nx\n        >>> from cdt.causality.graph import Fast_IAMB\n        >>> from cdt.data import load_dataset\n        >>> data, graph = load_dataset("sachs")\n        >>> obj = Fast_IAMB()\n        >>> #The predict() method works without a graph, or with a\n        >>> #directed or undirected graph provided as an input\n        >>> output = obj.predict(data)    #No graph provided as an argument\n        >>>\n        >>> output = obj.predict(data, nx.Graph(graph))  #With an undirected graph\n        >>>\n        >>> output = obj.predict(data, graph)  #With a directed graph\n        >>>\n        >>> #To view the graph created, run the below commands:\n        >>> nx.draw_networkx(output, font_size=8)\n        >>> plt.show()\n    '

    def __init__(self):
        super(Fast_IAMB, self).__init__()
        self.arguments['{ALGORITHM}'] = 'fast.iamb'


class Inter_IAMB(BNlearnAlgorithm):
    __doc__ = 'Interleaved IAMB algorithm.\n\n    **Description:** Similar to IAMB, Interleaved-IAMB has a progressive\n    forward selection minimizing false positives.\n\n    **Required R packages**: bnlearn\n\n    **Data Type:** Depends on the test used. Check\n    :ref:`here <bnlearntests>` for the list of available tests.\n\n    **Assumptions:** Inter-IAMB outputs markov blankets of nodes, with additional\n    assumptions depending on the conditional test used.\n\n    .. note::\n       Yaramakala S, Margaritis D (2005).  "Speculative Markov Blanket Discovery for Optimal Feature\n       Selection".  In "ICDM ’05:  Proceedings of the Fifth IEEE International Conference on Data Min-\n       ing", pp. 809-812. IEEE Computer Society.\n\n    Example:\n        >>> import networkx as nx\n        >>> from cdt.causality.graph import Inter_IAMB\n        >>> from cdt.data import load_dataset\n        >>> data, graph = load_dataset("sachs")\n        >>> obj = Inter_IAMB()\n        >>> #The predict() method works without a graph, or with a\n        >>> #directed or undirected graph provided as an input\n        >>> output = obj.predict(data)    #No graph provided as an argument\n        >>>\n        >>> output = obj.predict(data, nx.Graph(graph))  #With an undirected graph\n        >>>\n        >>> output = obj.predict(data, graph)  #With a directed graph\n        >>>\n        >>> #To view the graph created, run the below commands:\n        >>> nx.draw_networkx(output, font_size=8)\n        >>> plt.show()\n    '

    def __init__(self):
        super(Inter_IAMB, self).__init__()
        self.arguments['{ALGORITHM}'] = 'inter.iamb'


class MMPC(BNlearnAlgorithm):
    __doc__ = 'Max-Min Parents-Children algorithm.\n\n    **Description:** The Max-Min Parents-Children (MMPC) is a 2-phase algorithm\n    with a forward pass and a backward pass. The forward phase adds recursively\n    the variables that possess the highest association with the target\n    conditionally to the already selected variables. The backward pass tests\n    d-separability of variables conditionally to the set and subsets of the\n    selected variables.\n\n    **Required R packages**: bnlearn\n\n    **Data Type:** Depends on the test used. Check\n    :ref:`here <bnlearntests>` for the list of available tests.\n\n    **Assumptions:** MMPC outputs markov blankets of nodes, with additional\n    assumptions depending on the conditional test used.\n\n    .. note::\n       Tsamardinos I, Aliferis CF, Statnikov A (2003). "Time and Sample Efficient Discovery of Markov\n       Blankets and Direct Causal Relations".  In "KDD ’03:  Proceedings of the Ninth ACM SIGKDD\n       International Conference on Knowledge Discovery and Data Mining", pp. 673-678. ACM.\n       Tsamardinos I, Brown LE, Aliferis CF (2006).  "The Max-Min Hill-Climbing Bayesian Network\n       Structure Learning Algorithm".\n       Machine Learning,65(1), 31-78.\n\n    Example:\n        >>> import networkx as nx\n        >>> from cdt.causality.graph import MMPC\n        >>> from cdt.data import load_dataset\n        >>> data, graph = load_dataset("sachs")\n        >>> obj = MMPC()\n        >>> #The predict() method works without a graph, or with a\n        >>> #directed or undirected graph provided as an input\n        >>> output = obj.predict(data)    #No graph provided as an argument\n        >>>\n        >>> output = obj.predict(data, nx.Graph(graph))  #With an undirected graph\n        >>>\n        >>> output = obj.predict(data, graph)  #With a directed graph\n        >>>\n        >>> #To view the graph created, run the below commands:\n        >>> nx.draw_networkx(output, font_size=8)\n        >>> plt.show()\n    '

    def __init__(self):
        super(MMPC, self).__init__()
        self.arguments['{ALGORITHM}'] = 'mmpc'