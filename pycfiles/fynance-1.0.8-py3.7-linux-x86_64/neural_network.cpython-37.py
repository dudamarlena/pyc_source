# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fynance/models/neural_network.py
# Compiled at: 2019-09-26 11:10:55
# Size of source mod 2**32: 7258 bytes
""" Basis of neural networks models. """
import numpy as np, pandas as pd, torch, torch.nn
__all__ = [
 'BaseNeuralNet', 'MultiLayerPerceptron']

class BaseNeuralNet(torch.nn.Module):
    __doc__ = ' Base object for neural network model with PyTorch.\n\n    Inherits of torch.nn.Module object with some higher level methods.\n\n    Attributes\n    ----------\n    criterion : torch.nn.modules.loss\n        A loss function.\n    optimizer : torch.optim\n        An optimizer algorithm.\n    N, M : int\n        Respectively input and output dimension.\n\n    Methods\n    -------\n    set_optimizer\n    train_on\n    predict\n    set_data\n\n    See Also\n    --------\n    MultiLayerPerceptron, RollingBasis\n\n    '

    def __init__(self):
        """ Initialize. """
        torch.nn.Module.__init__(self)

    def set_optimizer(self, criterion, optimizer, **kwargs):
        """ Set the optimizer object.

        Set optimizer object with specified `criterion` as loss function and
        any `kwargs` as optional parameters.

        Parameters
        ----------
        criterion : torch.nn.modules.loss
            A loss function.
        optimizer : torch.optim
            An optimizer algorithm.
        **kwargs
            Keyword arguments of `optimizer`, cf PyTorch documentation [1]_.

        Returns
        -------
        BaseNeuralNet
            Self object model.

        References
        ----------
        .. [1] https://pytorch.org/docs/stable/optim.html

        """
        self.criterion = criterion()
        self.optimizer = optimizer((self.parameters()), **kwargs)
        return self

    @torch.enable_grad()
    def train_on(self, X, y):
        """ Trains the neural network model.

        Parameters
        ----------
        X, y : torch.Tensor
            Respectively inputs and outputs to train model.

        Returns
        -------
        torch.nn.modules.loss
            Loss outputs.

        """
        self.optimizer.zero_grad()
        outputs = self(X)
        loss = self.criterion(outputs, y)
        loss.backward()
        self.optimizer.step()
        return loss

    @torch.no_grad()
    def predict(self, X):
        """ Predicts outputs of neural network model.

        Parameters
        ----------
        X : torch.Tensor
           Inputs to compute prediction.

        Returns
        -------
        torch.Tensor
           Outputs prediction.

        """
        return self(X).detach()

    def set_data(self, X, y, x_type=None, y_type=None):
        """ Set data inputs and outputs.

        Parameters
        ----------
        X, y : array-like
            Respectively input and output data.
        x_type, y_type : torch.dtype
            Respectively input and ouput data types. Default is `None`.

        """
        if hasattr(self, 'N'):
            if self.N != X.size(1):
                raise ValueError('X must have {} input columns'.foramt(self.N))
        if hasattr(self, 'M'):
            if self.M != y.size(1):
                raise ValueError('y must have {} output columns'.format(self.M))
        self.X = self._set_data(X, dtype=x_type)
        self.y = self._set_data(y, dtype=y_type)
        self.T, self.N = self.X.size()
        T_veri, self.M = self.y.size()
        if self.T != T_veri:
            raise ValueError('{} time periods in X differents of {} time                              periods in y'.format(self.T, T_veri))
        return self

    def _set_data(self, X, dtype=None):
        """ Convert array-like data to tensor. """
        if isinstance(X, np.ndarray):
            return torch.from_numpy(X)
        if isinstance(X, pd.DataFrame):
            return torch.from_numpy(X.values)
        if isinstance(X, torch.Tensor):
            return X
        raise ValueError('Unkwnown data type: {}'.format(type(X)))


class MultiLayerPerceptron(BaseNeuralNet):
    __doc__ = ' Neural network with MultiLayer Perceptron architecture.\n\n    Refered as vanilla neural network model, with `n` hidden layers s.t\n    n :math:`\\geq` 1, with each one a specified number of neurons.\n\n    Parameters\n    ----------\n    X, y : array-like\n        Respectively inputs and outputs data.\n    layers : list of int\n        List of number of neurons in each hidden layer.\n    activation : torch.nn.Module\n        Activation function of layers.\n    drop : float, optional\n        Probability of an element to be zeroed.\n\n    Attributes\n    ----------\n    criterion : torch.nn.modules.loss\n        A loss function.\n    optimizer : torch.optim\n        An optimizer algorithm.\n    n : int\n        Number of hidden layers.\n    layers : list of int\n        List with the number of neurons for each hidden layer.\n    f : torch.nn.Module\n        Activation function.\n\n    Methods\n    -------\n    set_optimizer\n    train_on\n    predict\n    set_data\n\n    See Also\n    --------\n    BaseNeuralNet, RollMultiLayerPerceptron\n\n    '

    def __init__(self, X, y, layers=[], activation=None, drop=None, x_type=None, y_type=None, bias=True, activation_kwargs={}):
        """ Initialize object. """
        BaseNeuralNet.__init__(self)
        self.set_data(X=X, y=y, x_type=x_type, y_type=y_type)
        layers_list = []
        input_size = self.N
        for output_size in layers:
            layers_list += [
             torch.nn.Linear(input_size,
               output_size,
               bias=bias)]
            input_size = output_size

        layers_list += [torch.nn.Linear(input_size, (self.M), bias=bias)]
        self.layers = torch.nn.ModuleList(layers_list)
        if activation is not None:
            self.activation = activation(**activation_kwargs)
        else:
            self.activation = lambda x: x
        if drop is not None:
            self.drop = torch.nn.Dropout(p=drop)
        else:
            self.drop = lambda x: x

    def forward(self, x):
        """ Forward computation. """
        x = self.drop(x)
        for name, layer in enumerate(self.layers):
            x = self.activation(layer(x))

        return x


def _type_convert(dtype):
    if dtype is np.float64 or dtype is np.float or dtype is np.double:
        return torch.float64
    if dtype is np.float32:
        return torch.float32
    if dtype is np.float16:
        return torch.float16
    if dtype is np.uint8:
        return torch.uint8
    if dtype is np.int8:
        return torch.int8
    if dtype is np.int16 or dtype is np.short:
        return torch.int16
    if dtype is np.int32:
        return torch.int32
    if dtype is np.int64 or dtype is np.int or dtype is np.long:
        return torch.int64
    raise ValueError('Unkwnown type: {}'.format(str(dtype)))