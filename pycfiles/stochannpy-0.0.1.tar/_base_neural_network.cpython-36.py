# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\stochannpy\_base_neural_network.py
# Compiled at: 2018-02-07 04:12:49
# Size of source mod 2**32: 13498 bytes
"""
Author: Keurfon Luu <keurfon.luu@mines-paristech.fr>
License: MIT
"""
import numpy as np
from abc import ABCMeta, abstractmethod
from six import with_metaclass
from sklearn.base import BaseEstimator
from sklearn.utils import check_X_y, check_array, column_or_1d
from sklearn.utils.validation import check_is_fitted
from sklearn.preprocessing import LabelBinarizer
__all__ = [
 'BaseNeuralNetwork']

class BaseNeuralNetwork(with_metaclass(ABCMeta, BaseEstimator)):
    __doc__ = "\n    Base class for artifical neural network.\n    \n    Do not use this class, please use derived classes.\n    \n    Parameters\n    ----------\n    hidden_layer_sizes : tuple or list, length = n_layers-2, default (10,)\n        The ith element represents the number of neurons in the ith hidden\n        layer.\n    activation : {'logistic', 'tanh', 'relu'}, default 'relu'\n        Activation function the hidden layer.\n        - 'logistic', the logistic sigmoid function.\n        - 'tanh', the hyperbolic tan function.\n        - 'relu', the REctified Linear Unit function.\n    alpha : scalar, optional, default 0.\n        L2 penalty (regularization term) parameter.\n    max_iter : int, optional, default 100\n        Maximum number of iterations.\n    bounds : scalar, optional, default 1.\n        Search space boundaries for initialization.\n    random_state : int, optional, default None\n        Seed for random number generator.\n    "

    @abstractmethod
    def __init__(self, hidden_layer_sizes=(10,), activation='tanh', alpha=0.0, max_iter=100, bounds=1.0, random_state=None):
        self.hidden_layer_sizes = hidden_layer_sizes
        self.activation = activation
        self.alpha = alpha
        self.max_iter = max_iter
        self.bounds = bounds
        self.random_state = random_state

    def _validate_base_hyperparameters(self):
        if isinstance(self.hidden_layer_sizes, tuple) or isinstance(self.hidden_layer_sizes, list):
            if not np.all([isinstance(l, int) and l > 0 for l in self.hidden_layer_sizes]):
                raise ValueError('hidden_layer_sizes must contains positive integers only, got %s' % self.hidden_layer_sizes)
            else:
                raise ValueError('hidden_layer_sizes must be a tuple or a list')
            if not isinstance(self.activation, str):
                if self.activation not in ('logistic', 'tanh'):
                    raise ValueError("activation must either be 'logistic' or 'tanh', got %s" % self.activation)
            if not isinstance(self.alpha, float) and not isinstance(self.alpha, int) or self.alpha < 0.0:
                raise ValueError('alpha must be positive, got %s' % self.alpha)
            if not isinstance(self.max_iter, int) or self.max_iter <= 0:
                raise ValueError('max_iter must be a positive integer, got %s' % self.max_iter)
        else:
            if not isinstance(self.bounds, float) and not isinstance(self.bounds, int) or self.bounds <= 0.0:
                raise ValueError('bounds must be positive, got %s' % self.bounds)
            if self.random_state is not None:
                np.random.seed(self.random_state)

    def _validate_input(self, X, y):
        X, y = check_X_y(X, y)
        if y.ndim == 2:
            if y.shape[1] == 1:
                y = column_or_1d(y, warn=True)
        self._label_binarizer = LabelBinarizer()
        self._label_binarizer.fit(y)
        self.classes_ = self._label_binarizer.classes_
        y = self._label_binarizer.transform(y)
        return (X, y)

    def _initialize(self, X, y):
        hidden_layer_sizes = self.hidden_layer_sizes
        if not hasattr(hidden_layer_sizes, '__iter__'):
            hidden_layer_sizes = [
             hidden_layer_sizes]
        hidden_layer_sizes = list(hidden_layer_sizes)
        X, y = self._validate_input(X, y)
        self.ymat_ = np.array(y)
        self.n_samples_, self.n_features_ = X.shape
        self.n_outputs_ = y.shape[1]
        self.n_layers_ = len(hidden_layer_sizes) + 2
        self.layer_units_ = [self.n_features_] + hidden_layer_sizes + [self.n_outputs_]
        self.coef_indptr_ = []
        start = 0
        for i in range(self.n_layers_ - 1):
            n_fan_in, n_fan_out = self.layer_units_[i] + 1, self.layer_units_[(i + 1)]
            end = start + n_fan_in * n_fan_out
            self.coef_indptr_.append((start, end, (n_fan_out, n_fan_in)))
            start = end

        self._init_functions()
        return (X, y)

    def _predict(self, X):
        """
        Predict using the trained model.
        
        Parameters
        ----------
        X : ndarray of shape (n_samples, n_features)
            Input data.
        
        Returns
        -------
        h : ndarray
            Output layer activation values.
        """
        check_is_fitted(self, 'coefs_')
        X = check_array(X)
        unpacked_coefs = self.coefs_
        Z, activations = self._forward_pass(unpacked_coefs, X)
        return activations[(-1)]

    def _forward_pass(self, unpacked_coefs, X):
        """
        Perform a feedforward pass on the network.
        
        Parameters
        ----------
        unpacked_coefs : list of ndarray
            The ith element of the list holds the biases and weights of the
            ith layer.
        X : ndarray of shape (n_samples, n_features)
            Input data.
            
        Returns
        -------
        Z : list of ndarray
            Layers propagation matrices.
        activations : list of ndarray
            Layers activation values.
        """
        Z = [
         np.array([])]
        activations = [np.hstack((np.ones((X.shape[0], 1)), X))]
        for i in range(1, self.n_layers_ - 1):
            Z.append(np.dot(activations[(i - 1)], unpacked_coefs[(i - 1)].transpose()))
            activations.append(np.hstack((np.ones((Z[i].shape[0], 1)), self._func(Z[i]))))

        Z.append(np.dot(activations[(-1)], unpacked_coefs[(-1)].transpose()))
        activations.append(self._output_func(Z[(-1)]))
        activations[-1] = np.clip(activations[(-1)], 1e-10, 0.9999999999)
        return (Z, activations)

    def _backprop(self, Z, activations, unpacked_coefs):
        """
        Perform the backpropagation algorithm to compute the gradient.
        
        Parameters
        ----------
        Z : list of ndarray
            Layers propagation matrices.
        activations : list of ndarray
            Layers activation values.
        unpacked_coefs : list of ndarray
            The ith element of the list holds the biases and weights of the
            ith layer.
        
        Returns
        -------
        grad : list of ndarray
            The ith element of the list holds the gradient of the biases and
            weights of the ith layer.
        """
        sigma = [np.array([]) for i in range(self.n_layers_)]
        sigma[-1] = activations[(-1)] - self.ymat_
        for i in range(self.n_layers_ - 2, 0, -1):
            sigma[i] = np.dot(sigma[(i + 1)], unpacked_coefs[i]) * self._fprime(np.hstack((np.ones((Z[i].shape[0], 1)), Z[i])))
            sigma[i] = sigma[i][:, 1:]

        delta = []
        for i in range(self.n_layers_ - 1):
            delta.append(np.dot(sigma[(i + 1)].T, activations[i]))

        grad = []
        for i in range(self.n_layers_ - 1):
            grad.append(delta[i] / self.n_samples_ + self.alpha / self.n_samples_ * np.hstack((np.zeros((unpacked_coefs[i].shape[0], 1)), unpacked_coefs[i][:, 1:])))

        return grad

    def _loss(self, packed_coefs, X):
        """
        Compute the log loss function.
        
        Parameters
        ----------
        packed_coefs : ndarray
            Neural network biases and weights.
        X : ndarray of shape (n_samples, n_features)
            Input data.
            
        Returns
        -------
        loss : scalar
            Loss function value.
        """
        unpacked_coefs = self._unpack(packed_coefs)
        Z, activations = self._forward_pass(unpacked_coefs, X)
        values = np.sum(np.array([np.dot(s[:, 1:].ravel(), s[:, 1:].ravel()) for s in unpacked_coefs]))
        loss = np.sum(-self.ymat_ * np.log(activations[(-1)]) - (1.0 - self.ymat_) * np.log(1.0 - activations[(-1)]))
        loss += 0.5 * self.alpha * values
        loss /= self.n_samples_
        return loss

    def _grad(self, packed_coefs, X):
        """
        Compute the gradient of the loss function.
        
        Parameters
        ----------
        packed_coefs : ndarray
            Neural network biases and weights.
        X : ndarray of shape (n_samples, n_features)
            Input data.
            
        Returns
        -------
        grad : ndarray
            Gradient of neural network biases and weights.
        """
        unpacked_coefs = self._unpack(packed_coefs)
        Z, activations = self._forward_pass(unpacked_coefs, X)
        grad = self._backprop(Z, activations, unpacked_coefs)
        grad = self._pack(grad)
        return grad

    def _init_functions(self):
        if self.activation == 'logistic':
            self._func = self._sigmoid
            self._fprime = self._sigmoid_grad
        else:
            if self.activation == 'tanh':
                self._func = self._tanh
                self._fprime = self._tanh_grad
            else:
                if self.activation == 'relu':
                    self._func = self._relu
                    self._fprime = self._relu_grad
            if self._label_binarizer.y_type_ == 'multiclass':
                self._output_func = self._softmax
            else:
                self._output_func = self._sigmoid

    def _init_coefs(self):
        coefs_init = []
        for i in range(self.n_layers_ - 1):
            if self.activation == 'logistic':
                init_bound = np.sqrt(2.0 / (self.layer_units_[i] + self.layer_units_[(i + 1)] + 1))
            else:
                init_bound = np.sqrt(6.0 / (self.layer_units_[i] + self.layer_units_[(i + 1)] + 1))
            coefs_init.append(self._rand(self.layer_units_[(i + 1)], self.layer_units_[i] + 1, init_bound))

        return coefs_init

    def _rand(self, n1, n2, init_bound=1.0):
        """
        Generate uniform array between -init_bound and init_bound.
        
        Parameters
        ----------
        n1 : int
            First dimension of array.
        n2 : int
            Second dimension of array.
        init_bound : float, optional, default 1.
            Random number absolute maximum.
        
        Returns
        -------
        r : ndarray of shape (n1, n2)
            Uniform array between -init_bound and init_bound.
        """
        rnd = 2.0 * np.random.rand(n1, n2) - 1.0
        return init_bound * rnd

    def _sigmoid(self, x):
        out = np.array(x, dtype=(np.float64))
        return 0.5 * (1.0 + np.tanh(0.5 * out))

    def _sigmoid_grad(self, x):
        sig = self._sigmoid(x)
        return sig * (1 - sig)

    def _tanh(self, x):
        out = np.array(x, dtype=(np.float64))
        return np.tanh(out)

    def _tanh_grad(self, x):
        return 1.0 - self._tanh(x) ** 2

    def _relu(self, x):
        return np.clip(x, 0, np.finfo(x.dtype).max)

    def _relu_grad(self, x):
        return 1.0 * (np.array(x) > 0.0)

    def _softmax(self, x):
        tmp = x - x.max(axis=1)[:, np.newaxis]
        x = np.exp(tmp)
        x /= x.sum(axis=1)[:, np.newaxis]
        return x

    def _pack(self, unpacked_parameters):
        """
        Pack the coefficients into a 1-D array.
        
        Parameters
        ----------
        unpacked_parameters : list of ndarray
            The ith element of the list holds the biases and weights of the
            ith layer.
        
        Returns
        -------
        packed_parameters : ndarray
            Neural network biases and weights.
        """
        return np.hstack([l.ravel(order='F') for l in unpacked_parameters])

    def _unpack(self, packed_parameters):
        """
        Unpack the coefficients into a list of NumPy arrays.
        
        Parameters
        ----------
        packed_parameters : ndarray
            Neural network biases and weights.
        
        Returns
        -------
        unpacked_parameters : list of ndarray
            The ith element of the list holds the biases and weights of the
            ith layer.
        """
        unpacked_parameters = []
        for i in range(self.n_layers_ - 1):
            start, end, shape = self.coef_indptr_[i]
            unpacked_parameters.append(np.reshape((packed_parameters[start:end]), shape, order='F'))

        return unpacked_parameters