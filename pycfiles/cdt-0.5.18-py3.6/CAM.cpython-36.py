# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/causality/graph/CAM.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 8182 bytes
"""CAM algorithm.

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

class CAM(GraphModel):
    __doc__ = 'CAM algorithm **[R model]**.\n\n    **Description:** Causal Additive models, a causal discovery algorithm\n    relying on fitting Gaussian Processes on data, while considering all noises\n    additives and additive contributions of variables.\n\n    **Required R packages**: CAM\n\n    **Data Type:** Continuous\n\n    **Assumptions:** The data follows a generalized additive noise model:\n    each variable :math:`X_i`  in the graph :math:`\\mathcal{G}` is generated\n    following the model :math:`X_i = \\sum_{X_j \\in \\mathcal{G}} f(X_j) + \\epsilon_i`,\n    :math:`\\epsilon_i` representing mutually independent noises variables\n    accounting for unobserved variables.\n\n    Args:\n        score (str): Score used to fit the gaussian processes.\n        cutoff (float): threshold value for variable selection.\n        variablesel (bool): Perform a variable selection step.\n        selmethod (str): Method used for variable selection.\n        pruning (bool): Perform an initial pruning step.\n        prunmethod (str): Method used for pruning.\n        njobs (int): Number of jobs to run in parallel.\n        verbose (bool): Sets the verbosity of the output.\n\n    Available scores:\n       + nonlinear: \'SEMGAM\'\n       + linear: \'SEMLIN\'\n\n    Available variable selection methods:\n       + gamboost\': \'selGamBoost\'\n       + gam\': \'selGam\'\n       + lasso\': \'selLasso\'\n       + linear\': \'selLm\'\n       + linearboost\': \'selLmBoost\'\n\n    Default Parameters:\n       + FILE: \'/tmp/cdt_CAM/data.csv\'\n       + SCORE: \'SEMGAM\'\n       + VARSEL: \'TRUE\'\n       + SELMETHOD: \'selGamBoost\'\n       + PRUNING: \'TRUE\'\n       + PRUNMETHOD: \'selGam\'\n       + NJOBS: str(SETTINGS.NJOBS)\n       + CUTOFF: str(0.001)\n       + VERBOSE: \'FALSE\'\n       + OUTPUT: \'/tmp/cdt_CAM/result.csv\'\n\n    .. note::\n       Ref:\n       Bühlmann, P., Peters, J., & Ernest, J. (2014). CAM: Causal additive\n       models, high-dimensional order search and penalized regression. The\n       Annals of Statistics, 42(6), 2526-2556.\n\n    .. warning::\n       This implementation of CAM does not support starting with a graph.\n       The adaptation will be made at a later date.\n\n    Example:\n        >>> import networkx as nx\n        >>> from cdt.causality.graph import CAM\n        >>> from cdt.data import load_dataset\n        >>> data, graph = load_dataset("sachs")\n        >>> obj = CAM()\n        >>> output = obj.predict(data)\n    '

    def __init__(self, score='nonlinear', cutoff=0.001, variablesel=True, selmethod='gamboost', pruning=False, prunmethod='gam', njobs=None, verbose=None):
        """Init the model and its available arguments."""
        if not RPackages.CAM:
            raise ImportError('R Package CAM is not available.')
        super(CAM, self).__init__()
        self.scores = {'nonlinear':'SEMGAM',  'linear':'SEMLIN'}
        self.var_selection = {'gamboost':'selGamBoost',  'gam':'selGam', 
         'lasso':'selLasso', 
         'linear':'selLm', 
         'linearboost':'selLmBoost'}
        self.arguments = {'{FOLDER}':'/tmp/cdt_CAM/',  '{FILE}':'data.csv', 
         '{SCORE}':'SEMGAM', 
         '{VARSEL}':'TRUE', 
         '{SELMETHOD}':'selGamBoost', 
         '{PRUNING}':'TRUE', 
         '{PRUNMETHOD}':'selGam', 
         '{NJOBS}':str(SETTINGS.NJOBS), 
         '{CUTOFF}':str(0.001), 
         '{VERBOSE}':'FALSE', 
         '{OUTPUT}':'result.csv'}
        self.score = score
        self.cutoff = cutoff
        self.variablesel = variablesel
        self.selmethod = selmethod
        self.pruning = pruning
        self.prunmethod = prunmethod
        self.njobs = SETTINGS.get_default(njobs=njobs)
        self.verbose = SETTINGS.get_default(verbose=verbose)

    def orient_undirected_graph(self, data, graph, score='obs', verbose=False, **kwargs):
        """Run CAM on an undirected graph."""
        raise ValueError('CAM cannot (yet) be ran with a skeleton/directed graph.')

    def orient_directed_graph(self, data, graph, *args, **kwargs):
        """Run CAM on a directed_graph."""
        raise ValueError('CAM cannot (yet) be ran with a skeleton/directed graph.')

    def create_graph_from_data(self, data, **kwargs):
        """Apply causal discovery on observational data using CAM.

        Args:
            data (pandas.DataFrame): DataFrame containing the data

        Returns:
            networkx.DiGraph: Solution given by the CAM algorithm.
        """
        self.arguments['{SCORE}'] = self.scores[self.score]
        self.arguments['{CUTOFF}'] = str(self.cutoff)
        self.arguments['{VARSEL}'] = str(self.variablesel).upper()
        self.arguments['{SELMETHOD}'] = self.var_selection[self.selmethod]
        self.arguments['{PRUNING}'] = str(self.pruning).upper()
        self.arguments['{PRUNMETHOD}'] = self.var_selection[self.prunmethod]
        self.arguments['{NJOBS}'] = str(self.njobs)
        self.arguments['{VERBOSE}'] = str(self.verbose).upper()
        results = self._run_cam(data, verbose=(self.verbose))
        return nx.relabel_nodes(nx.DiGraph(results), {idx:i for idx, i in enumerate(data.columns)})

    def _run_cam(self, data, fixedGaps=None, verbose=True):
        """Setting up and running CAM with all arguments."""
        id = str(uuid.uuid4())
        os.makedirs('/tmp/cdt_CAM' + id + '/')
        self.arguments['{FOLDER}'] = '/tmp/cdt_CAM' + id + '/'

        def retrieve_result():
            return read_csv(('/tmp/cdt_CAM' + id + '/result.csv'), delimiter=',').values

        try:
            data.to_csv(('/tmp/cdt_CAM' + id + '/data.csv'), header=False, index=False)
            cam_result = launch_R_script(('{}/R_templates/cam.R'.format(os.path.dirname(os.path.realpath(__file__)))), (self.arguments),
              output_function=retrieve_result, verbose=verbose)
        except Exception as e:
            rmtree('/tmp/cdt_CAM' + id + '')
            raise e
        except KeyboardInterrupt:
            rmtree('/tmp/cdt_CAM' + id + '/')
            raise KeyboardInterrupt

        rmtree('/tmp/cdt_CAM' + id + '')
        return cam_result