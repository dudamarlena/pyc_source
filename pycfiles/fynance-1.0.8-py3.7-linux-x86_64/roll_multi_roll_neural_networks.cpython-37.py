# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fynance/neural_networks/roll_multi_roll_neural_networks.py
# Compiled at: 2019-02-20 14:01:28
# Size of source mod 2**32: 6932 bytes
import numpy as np
from matplotlib import pyplot as plt
from fynance.neural_networks.roll_multi_neural_networks import RollMultiNeuralNet
plt.style.use('seaborn')

class RollMultiRollNeuralNet(RollMultiNeuralNet):
    __doc__ = ' Rolling Multi Rolling Neural Networks object allow you to train \n    several rolling neural networks along training periods (from t - n to t) \n    and predict along testing periods (from t to t + s) and roll along this \n    time axis. And "sometime" it reseting parameters of one rolling neural \n    network.\n\n    Attributes\n    ----------\n    y : np.ndarray[np.float32, ndim=2] with shape=(T, 1)\n        Target to estimate or predict.\n    X : np.ndarray[np.float32, ndim=2] with shape=(T, N)\n        Features (inputs).\n    NN : list of keras.Model\n        Neural network models to train and predict.\n    y_train : np.ndarray[np.float64, ndim=1]\n        Prediction on training set.\n    y_estim : np.ndarray[np.float64, ndim=1]\n        Prediction on estimating set.\n\n\n    Methods\n    -------\n    run(y, X, NN, plot_loss=True, plot_perf=True, x_axis=None)\n        Train several rolling neural networks along pre-specified training \n        period and predict along test period. Display loss and performance \n        if specified.\n    __call__(y, X, NN, start=0, end=1e8, x_axis=None)\n        Callable method to set target and features data, neural network \n        object (Keras object is prefered).\n    __iter__()\n        Train and predict along time axis from day number n to last day \n        number T and by step of size s period. \n    plot_loss(self, f, ax)\n        Plot loss function\n    plot_perf(self, f, ax)\n        Plot perfomances.\n\n    See Also\n    --------\n    RollNeuralNet, RollAggrMultiNeuralNet, RollMultiNeuralNet\n\n    '

    def __call__(self, y, X, NN, weights=[], start=0, end=100000000.0, x_axis=None, reset_nn=True):
        """ Callable method to set terget and features data, neural network 
        object (Keras object is prefered).

        Parameters
        ----------
        y : np.ndarray[ndim=1, dtype=np.float32]
            Target to predict.
        X : np.ndarray[ndim=2, dtype=np.float32]
            Features data.
        NN : list of keras.engine.training.Model
            Neural network models.
        start : int
            Starting observation, default is first one.
        end : int
            Ending observation, default is last one.
        x_axis : np.ndarray[ndim=1], optional
            X-Axis to use for the backtest.
        reset_nn : bool or int, optional
            If int reset one neural network each `reset_nn` periods.
            Default is True.

        Returns
        -------
        rmrnn : RollMultiRollNeuralNet

        """
        RollMultiNeuralNet.__call__(self,
          y, X, NN, start=start, end=end, x_axis=x_axis)
        for i in range(len(weights)):
            self.NN[i].set_weights(weights[i])

        if reset_nn is not None:
            self.init_weights = []
            for nn in self.NN:
                self.init_weights += [nn.get_weights()]

        self.reset_nn = reset_nn
        self.count = 0
        return self

    def __next__(self):
        """ Incrementing method """
        self.t += self.s
        t = self.t
        if self.t >= self.T:
            raise StopIteration
        subtrain_X = self.X[t - self.n:t, :]
        subtrain_y = self.f(self.y[t - self.n:t, :])
        subestim_X = self.X[t:t + self.s, :]
        subestim_y = self.f(self.y[t:t + self.s, :])
        for i in range(self.n_NN):
            if self.reset_nn is not None:
                if self.count % (self.reset_nn * self.n_NN) == i * self.reset_nn:
                    self.NN[i].set_weights(self.init_weights[i])
            self.y_train[t - self.s:t, i] = self._train(y=subtrain_y,
              X=subtrain_X,
              i=i,
              val_set=(
             subestim_X, subestim_y))
            self.y_estim[t:t + self.s, i] = self.NN[i].predict(subestim_X).flatten()

        if self.reset_nn is not None:
            self.count += 1
        return (
         self.y_train[t - self.s:t, :], self.y_estim[t:t + self.s, :])

    def run(self, y, X, NN, weights=[], plot_loss=True, plot_perf=True, x_axis=None, reset_nn=True):
        """ Train several rolling neural networks along pre-specified train 
        period and predict along test period. Display loss and performance 
        if specified.
        
        Parameters
        ----------
        y : np.ndarray[np.float32, ndim=2] with shape=(T, 1)
            Time series of target to estimate or predict.
        X : np.ndarray[np.float32, ndim=2] with shape=(T, N)
            Several time series of features.
        NN : keras.Model or list of keras.Model
            Neural networks to train and predict.
        plot_loss : bool, optional
            If true dynamic plot of loss function, default is True.
        plot_perf : bool, optional
            If true dynamic plot of strategy performance, default is True.
        x_axis : list or array, optional
            x-axis to plot (e.g. list of dates).

        Returns
        -------
        rmrnn : RollMultiRollNeuralNet (object)

        """
        if isinstance(NN, list):
            self.n_NN = len(NN)
        else:
            self.n_NN = 1
        self.perf_train = self.V0 * np.ones([y.size, self.n_NN])
        self.perf_estim = self.V0 * np.ones([y.size, self.n_NN])
        f, ax_loss, ax_perf = self._set_figure(plot_loss, plot_perf)
        for pred_train, pred_estim in self(y,
          X, NN, weights=weights, x_axis=x_axis, reset_nn=reset_nn):
            t, s = self.t, self.s
            returns = np.sign(pred_train) * y[t - s:t]
            cum_ret = np.exp(np.cumsum(returns, axis=0))
            self.perf_train[t - s:t] = self.perf_train[(t - s - 1)] * cum_ret
            returns = np.sign(pred_estim) * y[t:t + s]
            cum_ret = np.exp(np.cumsum(returns, axis=0))
            self.perf_estim[t:t + s] = self.perf_estim[(t - 1)] * cum_ret
            self._dynamic_plot(f, ax_loss=ax_loss, ax_perf=ax_perf)

        return self