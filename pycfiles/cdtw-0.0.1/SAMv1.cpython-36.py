# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/causality/graph/SAMv1.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 17190 bytes
__doc__ = 'Structural Agnostic Model. Code of the first version of the SAM algorithm,\navailable at https://arxiv.org/abs/1803.04929v1\n\nAuthor: Diviyan Kalainathan, Olivier Goudet\nDate: 09/3/2018\n\n.. MIT License\n..\n.. Copyright (c) 2018 Diviyan Kalainathan\n..\n.. Permission is hereby granted, free of charge, to any person obtaining a copy\n.. of this software and associated documentation files (the "Software"), to deal\n.. in the Software without restriction, including without limitation the rights\n.. to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n.. copies of the Software, and to permit persons to whom the Software is\n.. furnished to do so, subject to the following conditions:\n..\n.. The above copyright notice and this permission notice shall be included in all\n.. copies or substantial portions of the Software.\n..\n.. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n.. IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n.. FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n.. AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n.. LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n.. OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n.. SOFTWARE.\n'
import math, torch as th, networkx as nx
from torch.utils.data import DataLoader
from .model import GraphModel
from ...utils.Settings import SETTINGS
from ...utils.parallel import parallel_run

class CNormalized_Linear(th.nn.Module):
    """CNormalized_Linear"""

    def __init__(self, in_features, out_features, bias=False):
        """Initialize the layer."""
        super(CNormalized_Linear, self).__init__()
        self.in_features = in_features
        self.out_features = out_features
        self.weight = th.nn.Parameter(th.Tensor(out_features, in_features))
        if bias:
            self.bias = th.nn.Parameter(th.Tensor(out_features))
        else:
            self.register_parameter('bias', None)
        self.reset_parameters()

    def reset_parameters(self):
        """Reset the parameters."""
        stdv = 1.0 / math.sqrt(self.weight.size(1))
        self.weight.data.uniform_(-stdv, stdv)
        if self.bias is not None:
            self.bias.data.uniform_(-stdv, stdv)

    def forward(self, input):
        """Feed-forward through the network."""
        return th.nn.functional.linear(input, self.weight.div(self.weight.pow(2).sum(0).sqrt()))

    def __repr__(self):
        """For print purposes."""
        return self.__class__.__name__ + '(' + 'in_features=' + str(self.in_features) + ', out_features=' + str(self.out_features) + ', bias=' + str(self.bias is not None) + ')'


class SAM_discriminator(th.nn.Module):
    """SAM_discriminator"""

    def __init__(self, sizes, zero_components=[], **kwargs):
        """Init the SAM discriminator."""
        super(SAM_discriminator, self).__init__()
        self.sht = kwargs.get('shortcut', False)
        activation_function = kwargs.get('activation_function', th.nn.ReLU)
        activation_argument = kwargs.get('activation_argument', None)
        batch_norm = kwargs.get('batch_norm', False)
        dropout = kwargs.get('dropout', 0.0)
        layers = []
        for i, j in zip(sizes[:-2], sizes[1:-1]):
            layers.append(th.nn.Linear(i, j))
            if batch_norm:
                layers.append(th.nn.BatchNorm1d(j))
            if dropout != 0.0:
                layers.append(th.nn.Dropout(p=dropout))
            if activation_argument is None:
                layers.append(activation_function())
            else:
                layers.append(activation_function(activation_argument))

        layers.append(th.nn.Linear(sizes[(-2)], sizes[(-1)]))
        self.layers = (th.nn.Sequential)(*layers)

    def forward(self, x):
        """Feed-forward the model."""
        return self.layers(x)


class SAM_block(th.nn.Module):
    """SAM_block"""

    def __init__(self, sizes, zero_components=[], **kwargs):
        """Initialize a generator."""
        super(SAM_block, self).__init__()
        activation_function = kwargs.get('activation_function', th.nn.Tanh)
        activation_argument = kwargs.get('activation_argument', None)
        batch_norm = kwargs.get('batch_norm', False)
        layers = []
        for i, j in zip(sizes[:-2], sizes[1:-1]):
            layers.append(CNormalized_Linear(i, j))
            if batch_norm:
                layers.append(th.nn.BatchNorm1d(j))
            if activation_argument is None:
                layers.append(activation_function())
            else:
                layers.append(activation_function(activation_argument))

        layers.append(th.nn.Linear(sizes[(-2)], sizes[(-1)]))
        self.layers = (th.nn.Sequential)(*layers)
        _filter = th.ones(1, sizes[0])
        for i in zero_components:
            _filter[:, i].zero_()

        self.register_buffer('_filter', _filter)
        self.fs_filter = th.nn.Parameter(_filter.data)

    def forward(self, x):
        """Feed-forward the model."""
        return self.layers(x * (self._filter * self.fs_filter).expand_as(x))


class SAM_generators(th.nn.Module):
    """SAM_generators"""

    def __init__(self, data_shape, zero_components, nh=200, batch_size=-1, device='cpu', **kwargs):
        """Init the model."""
        super(SAM_generators, self).__init__()
        if batch_size == -1:
            batch_size = data_shape[0]
        rows, self.cols = data_shape
        self.noise = []
        for i in range(self.cols):
            pname = 'noise_{}'.format(i)
            self.register_buffer(pname, th.FloatTensor(batch_size, 1).to(device))
            self.noise.append(getattr(self, pname))

        self.blocks = th.nn.ModuleList()
        for i in range(self.cols):
            self.blocks.append(SAM_block(
             [
              self.cols + 1, nh, 1], (zero_components[i]), **kwargs))

    def forward(self, x):
        """Feed-forward the model."""
        for i in self.noise:
            i.data.normal_()

        self.generated_variables = [self.blocks[i](th.cat([x, self.noise[i]], 1)) for i in range(self.cols)]
        return self.generated_variables


def run_SAM(df_data, skeleton=None, device=None, **kwargs):
    """Execute the SAM model.

    :param df_data: Input data; either np.array or pd.DataFrame
    """
    device = SETTINGS.get_default(device=device)
    train_epochs = kwargs.get('train_epochs', 1000)
    test_epochs = kwargs.get('test_epochs', 1000)
    batch_size = kwargs.get('batch_size', -1)
    lr_gen = kwargs.get('lr_gen', 0.1)
    lr_disc = kwargs.get('lr_disc', lr_gen)
    verbose = kwargs.get('verbose', True)
    regul_param = kwargs.get('regul_param', 0.1)
    dnh = kwargs.get('dnh', None)
    d_str = 'Epoch: {} -- Disc: {} -- Gen: {} -- L1: {}'
    try:
        list_nodes = list(df_data.columns)
        df_data = df_data[list_nodes].values
    except AttributeError:
        list_nodes = list(range(df_data.shape[1]))

    data = df_data.astype('float32')
    data = th.from_numpy(data)
    if batch_size == -1:
        batch_size = data.shape[0]
    else:
        rows, cols = data.size()
        if skeleton is not None:
            zero_components = [[] for i in range(cols)]
            skel = nx.adj_matrix(skeleton, weight=None)
            for i, j in zip(*(1 - skel).nonzero()):
                zero_components[j].append(i)

        else:
            zero_components = [[i] for i in range(cols)]
    sam = SAM_generators((rows, cols), zero_components, batch_norm=True, device=device, **kwargs)
    activation_function = kwargs.get('activation_function', th.nn.Tanh)
    try:
        del kwargs['activation_function']
    except KeyError:
        pass

    discriminator_sam = SAM_discriminator(
 [
  cols, dnh, dnh, 1], batch_norm=True, activation_function=th.nn.LeakyReLU, 
     activation_argument=0.2, **kwargs)
    kwargs['activation_function'] = activation_function
    sam = sam.to(device)
    discriminator_sam = discriminator_sam.to(device)
    data = data.to(device)
    criterion = th.nn.BCEWithLogitsLoss()
    g_optimizer = th.optim.Adam((sam.parameters()), lr=lr_gen)
    d_optimizer = th.optim.Adam((discriminator_sam.parameters()),
      lr=lr_disc)
    true_variable = th.ones(batch_size, 1)
    false_variable = th.zeros(batch_size, 1)
    causal_filters = th.zeros(data.shape[1], data.shape[1])
    true_variable = true_variable.to(device)
    false_variable = false_variable.to(device)
    causal_filters = causal_filters.to(device)
    data_iterator = DataLoader(data, batch_size=batch_size, shuffle=True)
    for epoch in range(train_epochs + test_epochs):
        for i_batch, batch in enumerate(data_iterator):
            batch_vectors = [batch[:, [i]] for i in range(cols)]
            g_optimizer.zero_grad()
            d_optimizer.zero_grad()
            generated_variables = sam(batch)
            disc_losses = []
            gen_losses = []
            for i in range(cols):
                generator_output = th.cat([v for c in [batch_vectors[:i],
                 [
                  generated_variables[i]],
                 batch_vectors[i + 1:]] for v in c], 1)
                disc_output_detached = discriminator_sam(generator_output.detach())
                disc_output = discriminator_sam(generator_output)
                disc_losses.append(criterion(disc_output_detached, false_variable))
                gen_losses.append(criterion(disc_output, true_variable))

            true_output = discriminator_sam(batch)
            adv_loss = sum(disc_losses) / cols + criterion(true_output, true_variable)
            gen_loss = sum(gen_losses)
            adv_loss.backward()
            d_optimizer.step()
            filters = th.stack([i.fs_filter[0, :-1].abs() for i in sam.blocks], 1)
            l1_reg = regul_param * filters.sum()
            loss = gen_loss + l1_reg
            if verbose:
                if epoch % 200 == 0:
                    if i_batch == 0:
                        print(str(i) + ' ' + d_str.format(epoch, adv_loss.item(), gen_loss.item() / cols, l1_reg.item()))
            loss.backward()
            if epoch > train_epochs:
                causal_filters.add_(filters.data)
            g_optimizer.step()

    return causal_filters.div_(test_epochs).cpu().numpy()


class SAMv1(GraphModel):
    """SAMv1"""

    def __init__(self, lr=0.1, dlr=0.1, l1=0.1, nh=50, dnh=200, train_epochs=1000, test_epochs=1000, batch_size=-1, nruns=6, njobs=None, gpus=None, verbose=None):
        """Init and parametrize the SAM model.

        """
        super(SAMv1, self).__init__()
        self.lr = lr
        self.dlr = dlr
        self.l1 = l1
        self.nh = nh
        self.dnh = dnh
        self.train = train_epochs
        self.test = test_epochs
        self.batch_size = batch_size
        self.nruns = nruns
        self.njobs = SETTINGS.get_default(njobs=njobs)
        self.gpus = SETTINGS.get_default(gpu=gpus)
        self.verbose = SETTINGS.get_default(verbose=verbose)

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
        if self.gpus > 0:
            list_out = parallel_run(run_SAM, data, njobs=(self.njobs), skeleton=graph,
              lr_gen=(self.lr),
              lr_disc=(self.dlr),
              regul_param=(self.l1),
              nh=(self.nh),
              dnh=(self.dnh),
              gpus=(self.gpus),
              train_epochs=(self.train),
              test_epochs=(self.test),
              batch_size=(self.batch_size),
              verbose=(self.verbose),
              nruns=(self.nruns))
        else:
            list_out = [run_SAM(data, skeleton=graph, lr_gen=(self.lr), lr_disc=(self.dlr), regul_param=(self.l1), nh=(self.nh), dnh=(self.dnh), device=None, train_epochs=(self.train), test_epochs=(self.test), batch_size=(self.batch_size), verbose=(self.verbose)) for idx in range(self.nruns)]
        if return_list_results:
            return list_out
        else:
            W = list_out[0]
            for w in list_out[1:]:
                W += w

            W /= self.nruns
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