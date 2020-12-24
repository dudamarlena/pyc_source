# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/causality/graph/CGNN.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 19402 bytes
__doc__ = 'Causal Generative Neural Networks.\n\nAuthor : Olivier Goudet & Diviyan Kalainathan\nRef : Causal Generative Neural Networks (https://arxiv.org/abs/1711.08936)\nDate : 09/5/17\n\n.. MIT License\n..\n.. Copyright (c) 2018 Diviyan Kalainathan\n..\n.. Permission is hereby granted, free of charge, to any person obtaining a copy\n.. of this software and associated documentation files (the "Software"), to deal\n.. in the Software without restriction, including without limitation the rights\n.. to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n.. copies of the Software, and to permit persons to whom the Software is\n.. furnished to do so, subject to the following conditions:\n..\n.. The above copyright notice and this permission notice shall be included in all\n.. copies or substantial portions of the Software.\n..\n.. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n.. IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n.. FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n.. AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n.. LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n.. OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n.. SOFTWARE.\n'
import networkx as nx, numpy as np, itertools, warnings, torch as th, pandas as pd
from copy import deepcopy
from tqdm import trange
from torch.utils.data import DataLoader
from sklearn.preprocessing import scale
from ..pairwise.GNN import GNN
from ...utils.loss import MMDloss
from ...utils.Settings import SETTINGS
from ...utils.graph import dagify_min_edge
from ...utils.parallel import parallel_run
from .model import GraphModel

def message_warning(msg, *a, **kwargs):
    """Ignore everything except the message."""
    return str(msg) + '\n'


warnings.formatwarning = message_warning

class CGNN_block(th.nn.Module):
    """CGNN_block"""

    def __init__(self, sizes):
        super(CGNN_block, self).__init__()
        layers = []
        for i, j in zip(sizes[:-2], sizes[1:-1]):
            layers.append(th.nn.Linear(i, j))
            layers.append(th.nn.ReLU())

        layers.append(th.nn.Linear(sizes[(-2)], sizes[(-1)]))
        self.layers = (th.nn.Sequential)(*layers)

    def forward(self, x):
        """Forward through the network."""
        return self.layers(x)

    def reset_parameters(self):
        for layer in self.layers:
            if hasattr(layer, 'reset_parameters'):
                layer.reset_parameters()


class CGNN_model(th.nn.Module):
    """CGNN_model"""

    def __init__(self, adj_matrix, batch_size, nh=20, device=None, confounding=False, initial_graph=None, **kwargs):
        """Init the model by creating the blocks and extracting the topological order."""
        super(CGNN_model, self).__init__()
        self.topological_order = [i for i in nx.topological_sort(nx.DiGraph(adj_matrix))]
        self.adjacency_matrix = adj_matrix
        self.confounding = confounding
        if initial_graph is None:
            self.i_adj_matrix = self.adjacency_matrix
        else:
            self.i_adj_matrix = initial_graph
        self.blocks = th.nn.ModuleList()
        self.generated = [None for i in range(self.adjacency_matrix.shape[0])]
        self.register_buffer('noise', th.zeros(batch_size, self.adjacency_matrix.shape[0]))
        if self.confounding:
            corr_noises = []
            for i, j in zip(*np.nonzero(self.i_adj_matrix)):
                if i < j:
                    pname = 'cnoise_{}'.format(i)
                    self.register_buffer(pname, th.FloatTensor(batch_size, 1))
                    corr_noises.append([(i, j), getattr(self, pname)])

            self.corr_noise = dict(corr_noises)
        self.criterion = MMDloss(batch_size).to(device)
        self.register_buffer('score', th.FloatTensor([0]))
        self.batch_size = batch_size
        for i in range(self.adjacency_matrix.shape[0]):
            if not confounding:
                self.blocks.append(CGNN_block([int(self.adjacency_matrix[:, i].sum()) + 1, nh, 1]))
            else:
                self.blocks.append(CGNN_block([
                 int(self.i_adj_matrix[:, i].sum()) + int(self.adjacency_matrix[:, i].sum()) + 1, nh, 1]))

    def forward(self):
        """Generate according to the topological order of the graph,
        outputs a batch of generated data of size batch_size.

        Returns:
            torch.Tensor: Generated data
        """
        self.noise.data.normal_()
        if not self.confounding:
            for i in self.topological_order:
                self.generated[i] = self.blocks[i](th.cat([v for c in [
                 [self.generated[j] for j in np.nonzero(self.adjacency_matrix[:, i])[0]],
                 [
                  self.noise[:, [i]]]] for v in c], 1))

        else:
            for i in self.topological_order:
                self.generated[i] = self.blocks[i](th.cat([v for c in [
                 [self.generated[j] for j in np.nonzero(self.adjacency_matrix[:, i])[0]],
                 [self.corr_noise[(min(i, j), max(i, j))] for j in np.nonzero(self.i_adj_matrix[:, i])[0]][self.noise[:, [i]]]] for v in c], 1))

        return th.cat(self.generated, 1)

    def run(self, dataset, train_epochs=1000, test_epochs=1000, verbose=None, idx=0, lr=0.01, dataloader_workers=0, **kwargs):
        """Run the CGNN on a given graph.

        Args:
            dataset (torch.utils.data.Dataset): True Data, on the same device as the model.
            train_epochs (int): number of train epochs
            test_epochs (int): number of test epochs
            verbose (bool): verbosity of the model
            idx (int): indicator for printing purposes
            lr (float): learning rate of the model
            dataloader_workers (int): number of workers

        Returns:
            float: Average score of the graph on `test_epochs` epochs
        """
        verbose = SETTINGS.get_default(verbose=verbose)
        optim = th.optim.Adam((self.parameters()), lr=lr)
        self.score.zero_()
        dataloader = DataLoader(dataset, batch_size=(self.batch_size), shuffle=True,
          drop_last=True,
          num_workers=dataloader_workers)
        with trange((train_epochs + test_epochs), disable=(not verbose)) as (t):
            for epoch in t:
                for i, data in enumerate(dataloader):
                    optim.zero_grad()
                    generated_data = self.forward()
                    mmd = self.criterion(generated_data, data)
                    if not epoch % 200:
                        if i == 0:
                            t.set_postfix(idx=idx, loss=(mmd.item()))
                        mmd.backward()
                        optim.step()
                        if epoch >= test_epochs:
                            self.score.add_(mmd.data)

        return self.score.cpu().numpy() / test_epochs

    def reset_parameters(self):
        for block in self.blocks:
            block.reset_parameters()


def graph_evaluation(data, adj_matrix, device='cpu', batch_size=-1, **kwargs):
    """Evaluate a graph taking account of the hardware."""
    if isinstance(data, th.utils.data.Dataset):
        obs = data.to(device)
    else:
        obs = th.Tensor(scale(data.values)).to(device)
    if batch_size == -1:
        batch_size = obs.__len__()
    cgnn = CGNN_model(adj_matrix, batch_size, **kwargs).to(device)
    cgnn.reset_parameters()
    return (cgnn.run)(obs, **kwargs)


def parallel_graph_evaluation(data, adj_matrix, nruns=16, njobs=None, gpus=None, **kwargs):
    """Parallelize the various runs of CGNN to evaluate a graph."""
    njobs, gpus = SETTINGS.get_default(('njobs', njobs), ('gpu', gpus))
    if gpus == 0:
        output = [graph_evaluation(data, adj_matrix, device=SETTINGS.default_device, **kwargs) for run in range(nruns)]
    else:
        output = parallel_run(graph_evaluation, data,
 adj_matrix, njobs=njobs, gpus=gpus, 
         nruns=nruns, **kwargs)
    return np.mean(output)


def hill_climbing(data, graph, **kwargs):
    """Hill Climbing optimization: a greedy exploration algorithm."""
    if isinstance(data, th.utils.data.Dataset):
        nodelist = data.get_names()
    else:
        if isinstance(data, pd.DataFrame):
            nodelist = list(data.columns)
        else:
            raise TypeError('Data type not understood')
    tested_candidates = [
     nx.adj_matrix(graph, nodelist=nodelist, weight=None)]
    best_score = parallel_graph_evaluation(data, 
     (tested_candidates[0].todense()), **kwargs)
    best_candidate = graph
    can_improve = True
    while can_improve:
        can_improve = False
        for i, j in best_candidate.edges():
            test_graph = deepcopy(best_candidate)
            test_graph.add_edge(j, i, weight=(test_graph[i][j]['weight']))
            test_graph.remove_edge(i, j)
            tadjmat = nx.adj_matrix(test_graph, nodelist=nodelist, weight=None)
            if nx.is_directed_acyclic_graph(test_graph) and not any([(tadjmat != cand).nnz == 0 for cand in tested_candidates]):
                tested_candidates.append(tadjmat)
                score = parallel_graph_evaluation(data, (tadjmat.todense()), **kwargs)
                if score < best_score:
                    can_improve = True
                    best_candidate = test_graph
                    best_score = score
                    break

    return best_candidate


class CGNN(GraphModel):
    """CGNN"""

    def __init__(self, nh=20, nruns=16, njobs=None, gpus=None, batch_size=-1, lr=0.01, train_epochs=1000, test_epochs=1000, verbose=None, dataloader_workers=0):
        """ Initialize the CGNN Model."""
        super(CGNN, self).__init__()
        self.nh = nh
        self.nruns = nruns
        self.njobs = SETTINGS.get_default(njobs=njobs)
        self.gpus = SETTINGS.get_default(gpu=gpus)
        self.lr = lr
        self.train_epochs = train_epochs
        self.test_epochs = test_epochs
        self.verbose = SETTINGS.get_default(verbose=verbose)
        self.batch_size = batch_size
        self.dataloader_workers = dataloader_workers

    def create_graph_from_data(self, data):
        """Use CGNN to create a graph from scratch. All the possible structures
        are tested, which leads to a super exponential complexity. It would be
        preferable to start from a graph skeleton for large graphs.

        Args:
            data (pandas.DataFrame or torch.utils.data.Dataset): Observational
               data on which causal discovery has to be performed.
        Returns:
            networkx.DiGraph: Solution given by CGNN.
        """
        warnings.warn('An exhaustive search of the causal structure of CGNN without skeleton is super-exponential in the number of variables.')
        if not isinstance(data, th.utils.data.Dataset):
            nb_vars = len(list(data.columns))
            names = list(data.columns)
        else:
            nb_vars = data.__featurelen__()
            names = data.get_names()
        candidates = [np.reshape(np.array(i), (nb_vars, nb_vars)) for i in itertools.product([0, 1], repeat=(nb_vars * nb_vars)) if np.trace(np.reshape(np.array(i), (nb_vars, nb_vars))) == 0 if nx.is_directed_acyclic_graph(nx.DiGraph(np.reshape(np.array(i), (nb_vars, nb_vars))))]
        warnings.warn('A total of {} graphs will be evaluated.'.format(len(candidates)))
        scores = [parallel_graph_evaluation(data, i, njobs=(self.njobs), nh=(self.nh), nruns=(self.nruns), gpus=(self.gpus), lr=(self.lr), train_epochs=(self.train_epochs), test_epochs=(self.test_epochs), verbose=(self.verbose), batch_size=(self.batch_size), dataloader_workers=(self.dataloader_workers)) for i in candidates]
        final_candidate = candidates[scores.index(min(scores))]
        output = np.zeros(final_candidate.shape)
        for (i, j), x in np.ndenumerate(final_candidate):
            if x > 0:
                cand = np.copy(final_candidate)
                cand[(i, j)] = 0
                output[(i, j)] = min(scores) - scores[[np.array_equal(cand, tgraph) for tgraph in candidates].index(True)]

        prediction = nx.DiGraph(final_candidate * output)
        return nx.relabel_nodes(prediction, {idx:i for idx, i in enumerate(names)})

    def orient_directed_graph(self, data, dag, alg='HC'):
        """Modify and improve a directed acyclic graph solution using CGNN.

        Args:
            data (pandas.DataFrame or torch.utils.data.Dataset): Observational
               data on which causal discovery has to be performed.
            dag (nx.DiGraph): Graph that provides the initial solution,
               on which the CGNN algorithm will be applied.
            alg (str): Exploration heuristic to use, only "HC" is supported for
               now.
        Returns:
            networkx.DiGraph: Solution given by CGNN.

        """
        alg_dic = {'HC': hill_climbing}
        return alg_dic[alg](data, dag, njobs=(self.njobs), nh=(self.nh), nruns=(self.nruns),
          gpus=(self.gpus),
          lr=(self.lr),
          train_epochs=(self.train_epochs),
          test_epochs=(self.test_epochs),
          verbose=(self.verbose),
          batch_size=(self.batch_size),
          dataloader_workers=(self.dataloader_workers))

    def orient_undirected_graph(self, data, umg, alg='HC'):
        """Orient the undirected graph using GNN and apply CGNN to improve the graph.

        Args:
            data (pandas.DataFrame): Observational data on which causal
               discovery has to be performed.
            umg (nx.Graph): Graph that provides the skeleton, on which the GNN
               then the CGNN algorithm will be applied.
            alg (str): Exploration heuristic to use, only "HC" is supported for
               now.
        Returns:
            networkx.DiGraph: Solution given by CGNN.

        .. note::
           GNN (``cdt.causality.pairwise.GNN``) is first used to orient the
           undirected graph and output a DAG before applying CGNN.
        """
        warnings.warn('The pairwise GNN model is computed on each edge of the UMG to initialize the model and start CGNN with a DAG')
        gnn = GNN(nh=(self.nh), lr=(self.lr), nruns=(self.nruns), njobs=(self.njobs),
          train_epochs=(self.train_epochs),
          test_epochs=(self.test_epochs),
          verbose=(self.verbose),
          gpus=(self.gpus),
          batch_size=(self.batch_size),
          dataloader_workers=(self.dataloader_workers))
        og = gnn.orient_graph(data, umg)
        dag = dagify_min_edge(og)
        return self.orient_directed_graph(data, dag, alg=alg)