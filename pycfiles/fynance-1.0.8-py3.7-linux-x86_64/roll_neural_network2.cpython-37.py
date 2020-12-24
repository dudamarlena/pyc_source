# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fynance/neural_networks/roll_neural_network2.py
# Compiled at: 2019-02-14 13:39:49
# Size of source mod 2**32: 12603 bytes
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from fynance.backtest.dynamic_plot_backtest import PlotBackTest
plt.style.use('seaborn')

class RollNeuralNet:
    __doc__ = ' Rolling Neural Network object allow you to train neural networks \n    along training periods (from t - n to t) and predict along testing \n    periods (from t to t + s) and roll along this time axis.\n\n    Attributes\n    ----------\n    y : np.ndarray[np.float32, ndim=2] with shape=(T, 1)\n        Target to estimate or predict.\n    X : np.ndarray[np.float32, ndim=2] with shape=(T, N)\n        Features (inputs).\n    NN : keras.Model\n        Neural network to train and predict.\n    y_train : np.ndarray[np.float64, ndim=1]\n        Prediction on training set.\n    y_estim : np.ndarray[np.float64, ndim=1]\n        Prediction on estimating set.\n\n    Methods\n    -------\n    run : Train rolling neural networks along pre-specified training \n        period and predict along test period. Display loss and performance if \n        specified.\n    __iter__ : Train and predict along time axis from day number n to last day \n        number T and by step of size s period. \n\n    '

    def __init__(self, train_period=252, estim_period=63, value_init=100, target_filter='sign', params=None):
        """ Init method sets size of training and predicting period, inital 
        value to backtest, a target filter and training parameters.

        Parameters
        ----------
        train_period : int
            Size of the training period. Default is 252 corresponding at one 
            year i.e 252 trading days.
        estim_period : int
            Size of the period to predict (is also the default rolling 
            period). Default is 63 corresponding at three months i.e 63 
            trading days.
        value_init : int
            Initial value to backtest strategy. Default is 100.
        target_filter : function, str or bool
            Function to filtering target. If True or 'sign' use np.sign() 
            function, if False doesn't filtering target. Default is 'sign'.
        params : dict
            Parameters for training periods

        """
        self.n = train_period
        self.s = estim_period
        self.V0 = value_init
        self._set_parameters(params)
        if target_filter or target_filter == 'sign':
            self.f = np.sign
        else:
            if target_filter is None:
                self.f = lambda x: x
            else:
                self.f = target_filter

    def __call__(self, y, X, NN, start=0, end=1000000.0, x_axis=None):
        """ Callable method to set terget and features data, neural network 
        object (Keras object is prefered).

        Parameters
        ----------
        y : np.ndarray[ndim=1, dtype=np.float32]
            Target to predict.
        X : np.ndarray[ndim=2, dtype=np.float32]
            Features data.
        NN : keras.engine.training.Model
            Neural network model.
        start : int
            Starting observation, default is first observation.
        end : int
            Ending observation, default is last observation.
        x_axis : np.ndarray[ndim=1]
            X-Axis to use for the backtest (int, date, str, etc.).

        Returns
        -------
        rnn : RollNeuralNet

        """
        self.y = y
        self.X = X
        self.NN = NN
        self.t = max(self.n, start)
        self.T = min(y.size, end)
        if x_axis is None:
            self.x_axis = range(self.T)
        else:
            self.x_axis = x_axis
        return self

    def __iter__(self):
        """ Set iterative method """
        self.y_train = np.zeros([self.T, 1])
        self.y_estim = np.zeros([self.T, 1])
        k = self.params['epochs'] * (self.T - self.t) // self.s
        self.loss_train = np.ones([k, 1])
        self.loss_estim = np.ones([k, 1])
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
        self.y_train[t - self.s:t, 0] = self._train(y=subtrain_y,
          X=subtrain_X,
          val_set=(
         subestim_X, subestim_y))
        self.y_estim[t:t + self.s, 0] = self.NN.predict(subestim_X).flatten()
        return (
         self.y_train[t - self.s:t], self.y_estim[t:t + self.s])

    def _train(self, y, X, val_set=None):
        """ Train method and return prediction on training set """
        k = self.params['epochs'] * ((self.t - self.n) // self.s - 1)
        k_1 = self.params['epochs'] * (self.t - self.n) // self.s
        hist = (self.NN.fit)(x=X, 
         y=y, validation_data=val_set, **self.params)
        self.loss_train[k:k_1, 0] = hist.history['loss']
        self.loss_estim[k:k_1, 0] = hist.history['val_loss']
        return self.NN.predict((X[-self.s:]),
          verbose=(self.params['verbose'])).flatten()

    def _set_parameters(self, params):
        """ Setting parameters to fit method of neural network. If is `None` 
        set as default parameters: `batch_size=train_period`, `epochs=1`, 
        `shuffle=False` and no verbosity.

        Parameters
        ----------
        params : dict
            Parameters for training periods
        
        Returns
        -------
        rnn : RollNeuralNet

        """
        if params is None:
            self.params = {'batch_size':self.n,  'epochs':1, 
             'shuffle':False, 
             'verbose':0}
        else:
            self.params = params
        return self

    def run(self, y, X, NN, plot_loss=True, plot_perf=True, x_axis=None):
        """ Train several rolling neural networks along pre-specified train 
        period and predict along test period. Display loss and performance 
        if specified.
        
        Parameters
        ----------
        y : np.ndarray[np.float32, ndim=2], with shape (T, 1)
            Time series of target to estimate or predict.
        X : np.ndarray[np.float32, ndim=2], with shape (T, N)
            Several time series of features.
        NN : keras.Model or list of keras.Model
            Neural networks to train and predict.
        plot_loss : bool
            If true dynamic plot of loss function.
        plot_perf : bool
            If true dynamic plot of strategy performance.
        x_axis : list or array
            x-axis to plot (e.g. list of dates).

        Returns
        -------
        :self: RollNeuralNet (object)

        """
        self.perf_train = self.V0 * np.ones([y.size, 1])
        self.perf_estim = self.V0 * np.ones([y.size, 1])
        f, ax_loss, ax_perf = self._set_figure(plot_loss, plot_perf)
        for pred_train, pred_estim in self(y, X, NN, x_axis=x_axis):
            t, s = self.t, self.s
            returns = np.sign(pred_train) * y[t - s:t]
            cum_ret = np.exp(np.cumsum(returns, axis=0))
            self.perf_train[t - s:t] = self.perf_train[(t - s - 1)] * cum_ret
            returns = np.sign(pred_estim) * y[t:t + s]
            cum_ret = np.exp(np.cumsum(returns, axis=0))
            self.perf_estim[t:t + s] = self.perf_estim[(t - 1)] * cum_ret
            self._dynamic_plot(f, ax_loss=ax_loss, ax_perf=ax_perf)

        return self

    def _dynamic_plot(self, f, ax_loss=None, ax_perf=None):
        """ Dynamic plot """
        if ax_loss is not None:
            k = self.params['epochs'] * (self.t - self.n) // self.s
            plot_loss(self.loss_estim[:k], self.loss_train[:k], f, ax_loss)
        if ax_perf is not None:
            t, t_s = self.t, min(self.t + self.s, self.T)
            perf_estim = self.perf_estim[:t_s]
            perf_train = self.perf_train[:t]
            x_estim = self.x_axis[:t_s]
            x_train = self.x_axis[:t]
            plot_perf(perf_estim, perf_train, x_estim, x_train, f, ax_perf)
        f.canvas.draw()
        return (f, ax_loss, ax_perf)

    def plot(start=0, end=-1, train=True):
        """ """
        f, ax_loss, ax_perf = _set_figure(True, True)
        if train:
            loss_train = self.loss_train[start:end]
            perf_train = self.perf_train[start:end - self.s]
            x_train = self.x_axis[start:end - self.s]
        else:
            loss_train, perf_train, x_train = (None, None, None)
        loss_estim = self.loss_estim[(start, end)]
        perf_estim = self.perf_estim[(start, end)]
        x_estim = self.x_axis[start:end]
        plot_loss(loss_estim, loss_train, f, ax_loss)
        plot_perf(perf_estim, perf_train, f, ax_perf)
        return self


def plot_loss(loss_estim, loss_train=None, f=None, ax=None):
    """ Plot loss function of training and estimating periods of neural
    network.
    
    Parameters
    ----------
    loss_estim : list
        Value of loss function at each epoch and estimation.
    loss_train : list
        Value of loss function at each epoch and train.
    fig : matplotlib.figure.Figure
        Figure to display backtest.
    ax : matplotlib.axes
        Axe(s) to display a part of backtest.

    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure to display backtest.
    ax : matplotlib.axes
        Axe(s) to display a part of backtest.
    
    """
    pl = fy.PlotLoss(fig=f,
      ax=ax,
      title='Model loss',
      ylabel='Loss',
      xlabel='Epoch',
      yscale='log',
      tick_params={'axis':'x', 
     'labelsize':10})
    pl.plot(loss_estim, names='Estim NN', col='BuGn', lw=2.0)
    if loss_train is not None:
        pl.plot(loss_train, names='Train NN', col='YlOrBr', lw=1.5)
    ax.legend(loc='upper right', ncol=2, fontsize=10, handlelength=0.8,
      columnspacing=0.5,
      frameon=True)
    return (
     f, ax)


def plot_perf(perf_estim, perf_train=None, f=None, ax=None):
    """ Plot performances of training and estimating periods of neural
    network.

    Parameters
    ----------
    perf_estim : list
        Value of performances on estimation period.
    perf_train : list
        Value of performances on train period.
    fig : matplotlib.figure.Figure
        Figure to display backtest.
    ax : matplotlib.axes
        Axe(s) to display a part of backtest.

    Returns
    -------
    fig : matplotlib.figure.Figure
        Figure to display backtest.
    ax : matplotlib.axes
        Axe(s) to display a part of backtest.

    """
    pp = PlotPerf(fig=f,
      ax=ax,
      xlabel='Date',
      yscale='log',
      tick_params={'axis':'x', 
     'rotation':30,  'labelsize':10})
    pp.plot(perf_estim, x_estim, names='Estim NN', col='GnBu', lw=1.7)
    if perf_train is not None:
        pp.plot(perf_train, x_train, names='Train NN', col='OrRd', lw=1.2)
    ax.legend(loc='upper left', ncol=2, fontsize=10, handlelength=0.8,
      columnspacing=0.5,
      frameon=True)
    return (
     f, ax)


def _set_figure(plot_loss, plot_perf):
    """ Set figure, axes and parameters for dynamic plot. """
    f, ax = plt.subplots((plot_loss + plot_perf), 1, figsize=(9, 6))
    plt.ion()
    if plot_loss:
        ax_loss, ax_perf = plot_perf or ax, None
    else:
        if not plot_loss:
            if plot_perf:
                ax_loss, ax_perf = None, ax
        elif plot_loss and plot_perf:
            ax_loss, ax_perf = ax
        else:
            ax_loss, ax_perf = (None, None)
    return (
     f, ax_loss, ax_perf)