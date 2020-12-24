# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/causality/graph/SAM.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 20012 bytes
__doc__ = 'Structural Agnostic Model.\n\nAuthor: Diviyan Kalainathan, Olivier Goudet\nDate: 09/3/2018\n\n.. MIT License\n..\n.. Copyright (c) 2018 Diviyan Kalainathan\n..\n.. Permission is hereby granted, free of charge, to any person obtaining a copy\n.. of this software and associated documentation files (the "Software"), to deal\n.. in the Software without restriction, including without limitation the rights\n.. to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n.. copies of the Software, and to permit persons to whom the Software is\n.. furnished to do so, subject to the following conditions:\n..\n.. The above copyright notice and this permission notice shall be included in all\n.. copies or substantial portions of the Software.\n..\n.. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n.. IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n.. FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n.. AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n.. LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n.. OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n.. SOFTWARE.\n'
import os, numpy as np, torch as th, pandas as pd, networkx as nx
from torch.utils.data import DataLoader
from tqdm import tqdm
from sklearn.preprocessing import scale
from .model import GraphModel
from ...utils.parallel import parallel_run
from ...utils.loss import notears_constr
from ...utils.torch import ChannelBatchNorm1d, MatrixSampler, Linear3D
from ...utils.Settings import SETTINGS

class SAM_generators(th.nn.Module):
    """SAM_generators"""

    def __init__(self, data_shape, nh, skeleton=None, linear=False):
        """Init the model."""
        super(SAM_generators, self).__init__()
        layers = []
        self.linear = linear
        nb_vars = data_shape[1]
        self.nb_vars = nb_vars
        if skeleton is None:
            skeleton = 1 - th.eye(nb_vars + 1, nb_vars)
        else:
            skeleton = th.cat([th.Tensor(skeleton), th.ones(1, nb_vars)], 1)
        if linear:
            self.input_layer = Linear3D((nb_vars, nb_vars + 1, 1))
        else:
            self.input_layer = Linear3D((nb_vars, nb_vars + 1, nh))
            layers.append(ChannelBatchNorm1d(nb_vars, nh))
            layers.append(th.nn.Tanh())
            self.output_layer = Linear3D((nb_vars, nh, 1))
        self.layers = (th.nn.Sequential)(*layers)
        self.register_buffer('skeleton', skeleton)

    def forward(self, data, noise, adj_matrix, drawn_neurons=None):
        """Forward through all the generators.

        Args:
            data (torch.Tensor): True data
            noise (torch.Tensor): Samples of noise variables
            adj_matrix (torch.Tensor): Sampled adjacency matrix
            drawn_neurons (torch.Tensor): Sampled matrix of active neurons

        Returns:
            torch.Tensor: Batch of generated data
        """
        if self.linear:
            output = self.input_layer(data, noise, adj_matrix * self.skeleton)
        else:
            output = self.output_layer(self.layers(self.input_layer(data, noise, adj_matrix * self.skeleton)), drawn_neurons)
        return output.squeeze(2)

    def reset_parameters(self):
        if not self.linear:
            self.output_layer.reset_parameters()
            for layer in self.layers:
                if hasattr(layer, 'reset_parameters'):
                    layer.reset_parameters()

        self.input_layer.reset_parameters()


class SAM_discriminator(th.nn.Module):
    """SAM_discriminator"""

    def __init__(self, nfeatures, dnh, hlayers=2, mask=None):
        super(SAM_discriminator, self).__init__()
        self.nfeatures = nfeatures
        layers = []
        layers.append(th.nn.Linear(nfeatures, dnh))
        layers.append(th.nn.BatchNorm1d(dnh))
        layers.append(th.nn.LeakyReLU(0.2))
        for i in range(hlayers - 1):
            layers.append(th.nn.Linear(dnh, dnh))
            layers.append(th.nn.BatchNorm1d(dnh))
            layers.append(th.nn.LeakyReLU(0.2))

        layers.append(th.nn.Linear(dnh, 1))
        self.layers = (th.nn.Sequential)(*layers)
        if mask is None:
            mask = th.eye(nfeatures, nfeatures)
        self.register_buffer('mask', mask.unsqueeze(0))

    def forward(self, input, obs_data=None):
        """Forward pass in the discriminator.

        Args:
            input (torch.Tensor): True Data or generated data
            obs_data (torch.Tensor): True data in the case of `input=generated` for padding.

        Returns:
            torch.Tensor: Output of the discriminator
        """
        if obs_data is not None:
            return [self.layers(i) for i in th.unbind(obs_data.unsqueeze(1) * (1 - self.mask) + input.unsqueeze(1) * self.mask, 1)]
        else:
            return self.layers(input)

    def reset_parameters(self):
        for layer in self.layers:
            if hasattr(layer, 'reset_parameters'):
                layer.reset_parameters()


def run_SAM(in_data, skeleton=None, device='cpu', train=5000, test=1000, batch_size=-1, lr_gen=0.001, lr_disc=0.01, lambda1=0.001, lambda2=1e-07, nh=None, dnh=None, verbose=True, losstype='fgan', dagstart=0, dagloss=False, dagpenalization=0.05, dagpenalization_increase=0.0, linear=False, hlayers=2, idx=0):
    list_nodes = list(in_data.columns)
    data = scale(in_data[list_nodes].values)
    nb_var = len(list_nodes)
    data = data.astype('float32')
    data = th.from_numpy(data).to(device)
    if batch_size == -1:
        batch_size = data.shape[0]
    rows, cols = data.size()
    if skeleton is not None:
        skeleton = th.from_numpy(skeleton.astype('float32'))
    else:
        sam = SAM_generators((batch_size, cols), nh, skeleton=skeleton, linear=linear).to(device)
        sam.reset_parameters()
        g_optimizer = th.optim.Adam((list(sam.parameters())), lr=lr_gen)
        if losstype != 'mse':
            discriminator = SAM_discriminator(cols, dnh, hlayers).to(device)
            discriminator.reset_parameters()
            d_optimizer = th.optim.Adam((discriminator.parameters()), lr=lr_disc)
            criterion = th.nn.BCEWithLogitsLoss()
        else:
            criterion = th.nn.MSELoss()
            disc_loss = th.zeros(1)
        graph_sampler = MatrixSampler(nb_var, mask=skeleton, gumbel=False).to(device)
        graph_sampler.weights.data.fill_(2)
        graph_optimizer = th.optim.Adam((graph_sampler.parameters()), lr=lr_gen)
        if not linear:
            neuron_sampler = MatrixSampler((nh, nb_var), mask=False, gumbel=True).to(device)
            neuron_optimizer = th.optim.Adam((list(neuron_sampler.parameters())), lr=lr_gen)
        _true = th.ones(1).to(device)
        _false = th.zeros(1).to(device)
        output = th.zeros(nb_var, nb_var).to(device)
        noise = th.randn(batch_size, nb_var).to(device)
        noise_row = th.ones(1, nb_var).to(device)
        data_iterator = DataLoader(data, batch_size=batch_size, shuffle=True,
          drop_last=True)
        if verbose:
            pbar = tqdm(range(train + test))
        else:
            pbar = range(train + test)
    for epoch in pbar:
        for i_batch, batch in enumerate(data_iterator):
            g_optimizer.zero_grad()
            graph_optimizer.zero_grad()
            if losstype != 'mse':
                d_optimizer.zero_grad()
            if not linear:
                neuron_optimizer.zero_grad()
            if not epoch > train:
                drawn_graph = graph_sampler()
                if not linear:
                    drawn_neurons = neuron_sampler()
                else:
                    drawn_neurons = None
            noise.normal_()
            generated_variables = sam(batch, noise, th.cat([drawn_graph, noise_row], 0), drawn_neurons)
            if losstype == 'mse':
                gen_loss = criterion(generated_variables, batch)
            else:
                disc_vars_d = discriminator(generated_variables.detach(), batch)
            disc_vars_g = discriminator(generated_variables, batch)
            true_vars_disc = discriminator(batch)
            if losstype == 'gan':
                disc_loss = sum([criterion(gen, _false.expand_as(gen)) for gen in disc_vars_d]) / nb_var + criterion(true_vars_disc, _true.expand_as(true_vars_disc))
                gen_loss = sum([criterion(gen, _true.expand_as(gen)) for gen in disc_vars_g])
            else:
                if losstype == 'fgan':
                    disc_loss = sum([th.mean(th.exp(gen - 1)) for gen in disc_vars_d]) / nb_var - th.mean(true_vars_disc)
                    gen_loss = -sum([th.mean(th.exp(gen - 1)) for gen in disc_vars_g])
                disc_loss.backward()
                d_optimizer.step()
            filters = graph_sampler.get_proba()
            struc_loss = lambda1 * drawn_graph.sum()
            func_loss = 0 if linear else lambda2 * drawn_neurons.sum()
            regul_loss = struc_loss + func_loss
            if dagloss:
                if epoch > train * dagstart:
                    dag_constraint = notears_constr(filters * filters)
                    loss = gen_loss + regul_loss + (dagpenalization + (epoch - train * dagstart) * dagpenalization_increase) * dag_constraint
                else:
                    loss = gen_loss + regul_loss
                if verbose:
                    if epoch % 20 == 0:
                        if i_batch == 0:
                            pbar.set_postfix(gen=(gen_loss.item() / cols), disc=(disc_loss.item()),
                              regul_loss=(regul_loss.item()),
                              tot=(loss.item()))
                if epoch < train + test - 1:
                    loss.backward(retain_graph=True)
                if epoch >= train:
                    output.add_(filters.data)
                g_optimizer.step()
                graph_optimizer.step()
                if not linear:
                    neuron_optimizer.step()

    return output.div_(test).cpu().numpy()


class SAM(GraphModel):
    """SAM"""

    def __init__(self, lr=0.01, dlr=0.01, lambda1=0.01, lambda2=1e-05, nh=200, dnh=200, train_epochs=10000, test_epochs=1000, batchsize=-1, losstype='fgan', dagstart=0.5, dagloss=True, dagpenalization=0, dagpenalization_increase=0.001, linear=False, hlayers=2, njobs=None, gpus=None, verbose=None, nruns=8):
        """Init and parametrize the SAM model."""
        super(SAM, self).__init__()
        self.lr = lr
        self.dlr = dlr
        self.lambda1 = lambda1
        self.lambda2 = lambda2
        self.nh = nh
        self.dnh = dnh
        self.train = train_epochs
        self.test = test_epochs
        self.batchsize = batchsize
        self.losstype = losstype
        self.dagstart = dagstart
        self.dagloss = dagloss
        self.dagpenalization = dagpenalization
        self.dagpenalization_increase = dagpenalization_increase
        self.linear = linear
        self.hlayers = hlayers
        self.njobs = SETTINGS.get_default(njobs=njobs)
        self.gpus = SETTINGS.get_default(gpu=gpus)
        self.verbose = SETTINGS.get_default(verbose=verbose)
        self.nruns = nruns

    def predict(self, data, graph=None, return_list_results=False):
        """Execute SAM on a dataset given a skeleton or not.

        Args:
            data (pandas.DataFrame): Observational data for estimation of causal relationships by SAM
            skeleton (numpy.ndarray): A priori knowledge about the causal relationships as an adjacency matrix.
                      Can be fed either directed or undirected links.
        Returns:
            networkx.DiGraph: Graph estimated by SAM, where A[i,j] is the term
            of the ith variable for the jth generator.
        """
        if graph is not None:
            skeleton = th.Tensor(nx.adjacency_matrix(graph, nodelist=(list(data.columns))).todense())
        else:
            skeleton = None
        if not self.nruns > 0:
            raise AssertionError
        else:
            if self.gpus == 0:
                results = [run_SAM(data, skeleton=skeleton, lr_gen=(self.lr), lr_disc=(self.dlr), verbose=(self.verbose), lambda1=(self.lambda1), lambda2=(self.lambda2), nh=(self.nh), dnh=(self.dnh), train=(self.train), test=(self.test), batch_size=(self.batchsize), dagstart=(self.dagstart), dagloss=(self.dagloss), dagpenalization=(self.dagpenalization), dagpenalization_increase=(self.dagpenalization_increase), losstype=(self.losstype), linear=(self.linear), hlayers=(self.hlayers), device='cpu') for i in range(self.nruns)]
            else:
                results = parallel_run(run_SAM, data, skeleton=skeleton, nruns=(self.nruns),
                  njobs=(self.njobs),
                  gpus=(self.gpus),
                  lr_gen=(self.lr),
                  lr_disc=(self.dlr),
                  verbose=(self.verbose),
                  lambda1=(self.lambda1),
                  lambda2=(self.lambda2),
                  nh=(self.nh),
                  dnh=(self.dnh),
                  train=(self.train),
                  test=(self.test),
                  batch_size=(self.batchsize),
                  dagstart=(self.dagstart),
                  dagloss=(self.dagloss),
                  dagpenalization=(self.dagpenalization),
                  dagpenalization_increase=(self.dagpenalization_increase),
                  losstype=(self.losstype),
                  linear=(self.linear),
                  hlayers=(self.hlayers))
        list_out = [i for i in results if not np.isnan(i).any()]
        try:
            assert len(list_out) > 0
        except AssertionError as e:
            print('All solutions contain NaNs')
            raise e

        W = sum(list_out) / len(list_out)
        return nx.relabel_nodes(nx.DiGraph(W), {idx:i for idx, i in enumerate(data.columns)})

    def orient_directed_graph(self, *args, **kwargs):
        """Orient a (partially directed) graph."""
        return (self.predict)(*args, **kwargs)

    def orient_undirected_graph(self, *args, **kwargs):
        """Orient a undirected graph."""
        return (self.predict)(*args, **kwargs)

    def create_graph_from_data(self, *args, **kwargs):
        """Estimate a causal graph out of observational data."""
        return (self.predict)(*args, **kwargs)