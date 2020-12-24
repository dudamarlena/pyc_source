# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/independence/graph/FSGNN.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 10934 bytes
__doc__ = 'Feature selection model with generative models.\n\nAlgorithm between SAM and CGNN\nAuthor : Diviyan Kalainathan & Olivier Goudet\n\n.. MIT License\n..\n.. Copyright (c) 2018 Diviyan Kalainathan\n..\n.. Permission is hereby granted, free of charge, to any person obtaining a copy\n.. of this software and associated documentation files (the "Software"), to deal\n.. in the Software without restriction, including without limitation the rights\n.. to use, copy, modify, merge, publish, distribute, sublicense, and/or sell\n.. copies of the Software, and to permit persons to whom the Software is\n.. furnished to do so, subject to the following conditions:\n..\n.. The above copyright notice and this permission notice shall be included in all\n.. copies or substantial portions of the Software.\n..\n.. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\n.. IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\n.. FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\n.. AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\n.. LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\n.. OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\n.. SOFTWARE.\n'
import torch as th, numpy as np, networkx as nx
from torch.utils.data import Dataset, TensorDataset
from sklearn.preprocessing import scale
from tqdm import trange
from .model import FeatureSelectionModel
from ...utils.Settings import SETTINGS
from ...utils.loss import MMDloss
from ...utils.parallel import parallel_run_generator

class FSGNN_model(th.nn.Module):
    """FSGNN_model"""

    def __init__(self, sizes, dropout=0.0, activation_function=th.nn.ReLU):
        super(FSGNN_model, self).__init__()
        layers = []
        for i, j in zip(sizes[:-2], sizes[1:-1]):
            layers.append(th.nn.Linear(i, j))
            if dropout != 0.0:
                layers.append(th.nn.Dropout(p=dropout))
            layers.append(activation_function())

        layers.append(th.nn.Linear(sizes[(-2)], sizes[(-1)]))
        self.layers = (th.nn.Sequential)(*layers)
        self.sizes = sizes

    def forward(self, x):
        """Forward pass in the network.

        Args:
            x (torch.Tensor): input data

        Returns:
            torch.Tensor: output of the network
        """
        self.layers(x)

    def train(self, dataset, lr=0.01, l1=0.1, batch_size=-1, train_epochs=1000, test_epochs=1000, device=None, verbose=None, dataloader_workers=0):
        """Train the network and output the scores of the features

        Args:
            dataset (torch.utils.data.Dataset): Original data
            lr (float): Learning rate
            l1 (float): Coefficient of the L1 regularization
            batch_size (int): Batch size of the model, defaults to the dataset size.
            train_epochs (int): Number of train epochs
            test_epochs (int): Number of test epochs
            device (str): Device on which the computation is to be run
            verbose (bool): Verbosity of the model
            dataloader_workers (int): Number of workers for dataset loading

        Returns:
            list: feature selection scores for each feature.
        """
        device, verbose = SETTINGS.get_default(('device', device), ('verbose', verbose))
        optim = th.optim.Adam((self.parameters()), lr=lr)
        output = th.zeros(self.sizes[0] - 1).to(device)
        if batch_size == -1:
            batch_size = dataset.__len__()
        criterion = MMDloss(input_size=batch_size).to(device)
        noise = th.randn(batch_size, 1).to(device)
        data_iterator = th.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True,
          drop_last=True,
          num_workers=dataloader_workers)
        with trange((train_epochs + test_epochs), disable=(not verbose)) as (t):
            for epoch in t:
                for i, (batch, target) in enumerate(data_iterator):
                    optim.zero_grad()
                    noise.normal_()
                    gen = self.layers(th.cat([batch, noise], 1))
                    loss = criterion(gen, target) + l1 * (self.layers[0].weight.abs().sum() + self.layers[2].weight.abs().sum())
                    if not epoch % 100:
                        if i == 0:
                            t.set_postfix(epoch=epoch, loss=(loss.item()))
                    if epoch >= train_epochs:
                        output.add_(self.layers[0].weight.data[:, :-1].sum(dim=0))
                    loss.backward()
                    optim.step()

        return list(output.div_(test_epochs).div_(dataset.__len__() // batch_size).cpu().numpy())


class FSGNN(FeatureSelectionModel):
    """FSGNN"""

    def __init__(self, nh=20, dropout=0.0, activation_function=th.nn.ReLU, lr=0.01, l1=0.1, batch_size=-1, train_epochs=1000, test_epochs=1000, verbose=None, nruns=3, dataloader_workers=0, njobs=None):
        """Init the model."""
        super(FSGNN, self).__init__()
        self.nh = nh
        self.dropout = dropout
        self.activation_function = activation_function
        self.lr = lr
        self.l1 = l1
        self.batch_size = batch_size
        self.train_epochs = train_epochs
        self.test_epochs = test_epochs
        self.verbose = SETTINGS.get_default(verbose=verbose)
        self.nruns = nruns
        self.njobs = SETTINGS.get_default(njobs=njobs)
        self.dataloader_workers = dataloader_workers

    def predict_features(self, df_features, df_target, datasetclass=TensorDataset, device=None, idx=0):
        """For one variable, predict its neighbours.

        Args:
            df_features (pandas.DataFrame): Features to select
            df_target (pandas.Series): Target variable to predict
            datasetclass (torch.utils.data.Dataset): Class to override for
               custom loading of data.
            idx (int): (optional) for printing purposes
            device (str): cuda or cpu device (defaults to
               ``cdt.SETTINGS.default_device``)

        Returns:
            list: scores of each feature relatively to the target

        """
        device = SETTINGS.get_default(device=device)
        dataset = datasetclass(th.Tensor(scale(df_features.values)).to(device), th.Tensor(scale(df_target.values)).to(device))
        out = []
        for i in range(self.nruns):
            model = FSGNN_model([df_features.shape[1] + 1, self.nh, 1], activation_function=(self.activation_function),
              dropout=(self.dropout)).to(device)
            out.append(model.train(dataset, lr=0.01, l1=0.1, batch_size=(self.batch_size),
              train_epochs=(self.train_epochs),
              test_epochs=(self.test_epochs),
              device=device,
              verbose=(self.verbose),
              dataloader_workers=(self.dataloader_workers)))

        return list(np.mean((np.array(out)), axis=0))

    def predict(self, df_data, threshold=0.05, gpus=None, **kwargs):
        """Predict the skeleton of the graph from raw data.

        Returns iteratively the feature selection algorithm on each node.

        Args:
            df_data (pandas.DataFrame): data to construct a graph from
            threshold (float): cutoff value for feature selection scores
            kwargs (dict): additional arguments for algorithms

        Returns:
            networkx.Graph: predicted skeleton of the graph.
        """
        njobs = self.njobs
        gpus = SETTINGS.get_default(gpu=gpus)
        list_nodes = list(df_data.columns.values)
        if gpus > 0:
            result_feature_selection = parallel_run_generator((self.run_feature_selection), [([df_data, node], kwargs) for node in list_nodes],
              gpus=gpus,
              njobs=njobs)
        else:
            result_feature_selection = [(self.run_feature_selection)(df_data, node, idx, **kwargs) for idx, node in enumerate(list_nodes)]
        for idx, i in enumerate(result_feature_selection):
            try:
                i.insert(idx, 0)
            except AttributeError:
                result_feature_selection[idx] = np.insert(i, idx, 0)

        matrix_results = np.array(result_feature_selection)
        matrix_results *= matrix_results.transpose()
        np.fill_diagonal(matrix_results, 0)
        matrix_results /= 2
        graph = nx.Graph()
        for (i, j), x in np.ndenumerate(matrix_results):
            if matrix_results[(i, j)] > threshold:
                graph.add_edge((list_nodes[i]), (list_nodes[j]), weight=(matrix_results[(i, j)]))

        for node in list_nodes:
            if node not in graph.nodes():
                graph.add_node(node)

        return graph