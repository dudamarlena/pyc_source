# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\stochannpy\evolutionary_neural_network.py
# Compiled at: 2018-04-03 09:30:57
# Size of source mod 2**32: 11796 bytes
"""
Author: Keurfon Luu <keurfon.luu@mines-paristech.fr>
License: MIT
"""
import numpy as np
from sklearn.base import ClassifierMixin
from ._base_neural_network import BaseNeuralNetwork
from stochopy import Evolutionary
__all__ = [
 'ENNClassifier']

class ENNClassifier(BaseNeuralNetwork, ClassifierMixin):
    __doc__ = "\n    Evolutionary neural network classifier.\n    \n    This model optimizes the log-loss function using Differential Evolution,\n    Particle Swarm Optimization of Covariance Matrix Adaptation - Evolution\n    Strategy.\n    \n    Parameters\n    ----------\n    hidden_layer_sizes : tuple or list, length = n_layers-2, default (10,)\n        The ith element represents the number of neurons in the ith hidden\n        layer.\n    activation : {'logistic', 'tanh', 'relu'}, default 'relu'\n        Activation function the hidden layer.\n        - 'logistic', the logistic sigmoid function.\n        - 'tanh', the hyperbolic tan function.\n        - 'relu', the REctified Linear Unit function.\n    alpha : scalar, optional, default 0.\n        L2 penalty (regularization term) parameter.\n    max_iter : int, optional, default 100\n        Maximum number of iterations.\n    solver : {'de', 'pso', 'cpso', 'cmaes', 'vdcma'}, default 'cpso'\n        Evolutionary Algorithm optimizer.\n    popsize : int, optional, default 10\n        Population size.\n    w : scalar, optional, default 0.7298\n        Inertial weight. Only used when solver = {'pso', 'cpso'}.\n    c1 : scalar, optional, default 1.49618\n        Cognition parameter. Only used when solver = {'pso', 'cpso'}.\n    c2 : scalar, optional, default 1.49618\n        Sociability parameter. Only used when solver = {'pso', 'cpso'}.\n    gamma : scalar, optional, default 1.\n        Competitivity parameter. Only used when solver = 'cpso'.\n    delta : None or scalar, optional, default None\n        Swarm maximum radius. Only used when solver = 'cpso'.\n    F : scalar, optional, default 1.\n        Differential weight. Only used when solver = 'de'.\n    CR : scalar, optional, default 0.5\n        Crossover probability. Only used when solver = 'de'.\n    sigma : scalar, optional, default 1.\n        Step size. Only used when solver = {'cmaes', 'vdcma'}.\n    mu_perc : scalar, optional, default 0.5\n        Number of parents as a percentage of population size. Only used\n        when solver = {'cmaes', 'vdcma'}.\n    eps1 : scalar, optional, default 1e-8\n        Minimum change in best individual.\n    eps2 : scalar, optional, default 1e-8\n        Minimum objective function precision.\n    bounds : scalar, optional, default 1.\n        Search space boundaries for initialization.\n    random_state : int, optional, default None\n        Seed for random number generator.\n    \n    Examples\n    --------\n    Import the module and initialize the classifier:\n    \n    >>> import numpy as np\n    >>> from stochannpy import ENNClassifier\n    >>> clf = ENNClassifier(hidden_layer_sizes = (5,))\n    \n    Fit the training set:\n    \n    >>> clf.fit(X_train, y_train)\n    \n    Predict the test set:\n    \n    >>> ypred = clf.predict(X_test)\n    \n    Compute the accuracy:\n    \n    >>> print(np.mean(ypred == y_test))\n    "

    def __init__(self, hidden_layer_sizes=(10,), max_iter=100, alpha=0.0, activation='relu', solver='cpso', popsize=10, w=0.7298, c1=1.49618, c2=1.49618, gamma=1.0, F=1.0, CR=0.5, sigma=1.0, mu_perc=0.5, eps1=1e-08, eps2=1e-08, bounds=1.0, random_state=None):
        super(ENNClassifier, self).__init__(hidden_layer_sizes=hidden_layer_sizes,
          activation=activation,
          alpha=alpha,
          max_iter=max_iter,
          bounds=bounds,
          random_state=random_state)
        self.solver = solver
        self.popsize = int(popsize)
        self.eps1 = eps1
        self.eps2 = eps2
        self.w = w
        self.c1 = c1
        self.c2 = c2
        self.gamma = gamma
        self.F = F
        self.CR = CR
        self.sigma = sigma
        self.mu_perc = mu_perc

    def _validate_hyperparameters(self):
        self._validate_base_hyperparameters()
        if not isinstance(self.solver, str) or self.solver not in ('cpso', 'pso', 'de',
                                                                   'cmaes', 'vdcma'):
            raise ValueError("solver must either be 'cpso', 'pso', 'de', 'cmaes' or 'vdcma', got %s" % self.solver)
        if not isinstance(self.popsize, int) or self.popsize < 2:
            raise ValueError('popsize must be an integer > 1, got %s' % self.popsize)
        if not isinstance(self.eps1, float) and not isinstance(self.eps1, int) or self.eps1 < 0.0:
            raise ValueError('eps1 must be positive, got %s' % self.eps1)
        if not isinstance(self.eps2, float):
            if not isinstance(self.eps2, int):
                raise ValueError('eps2 must be an integer or float, got %s' % self.eps2)

    def fit(self, X, y):
        """
        Fit the model to data matrix X and target y.
        
        Parameters
        ----------
        X : ndarray of shape (n_samples, n_features)
            Input data.
        y : ndarray of length n_samples
            Target values.
        
        Returns
        -------
        self : returns a trained ENNClassifier.
        """
        self._validate_hyperparameters()
        X, y = self._initialize(X, y)
        n_dim = np.sum([np.prod(i[(-1)]) for i in self.coef_indptr_])
        lower = np.full(n_dim, -self.bounds)
        upper = np.full(n_dim, self.bounds)
        ea = Evolutionary((self._loss), lower=lower,
          upper=upper,
          max_iter=(self.max_iter),
          popsize=(self.popsize),
          eps1=(self.eps1),
          eps2=(self.eps2),
          constrain=False,
          args=(
         X,))
        if self.solver == 'de':
            packed_coefs, self.loss_ = ea.optimize(solver='de', F=(self.F),
              CR=(self.CR))
        else:
            if self.solver == 'pso':
                packed_coefs, self.loss_ = ea.optimize(solver='pso', w=(self.w),
                  c1=(self.c1),
                  c2=(self.c2))
            else:
                if self.solver == 'cpso':
                    packed_coefs, self.loss_ = ea.optimize(solver='cpso', w=(self.w),
                      c1=(self.c1),
                      c2=(self.c2),
                      gamma=(self.gamma))
                else:
                    if self.solver == 'cmaes':
                        packed_coefs, self.loss_ = ea.optimize(solver='cmaes', sigma=(self.sigma),
                          mu_perc=(self.mu_perc))
                    else:
                        if self.solver == 'vdcma':
                            packed_coefs, self.loss_ = ea.optimize(solver='vdcma', sigma=(self.sigma),
                              mu_perc=(self.mu_perc))
        self.coefs_ = self._unpack(packed_coefs)
        self.flag_ = ea.flag
        self.n_iter_ = ea.n_iter
        self.n_eval_ = ea.n_eval
        return self

    def predict(self, X):
        """
        Predict using the trained model.
        
        Parameters
        ----------
        X : ndarray of shape (n_samples, n_features)
            Input data.
        
        Returns
        -------
        ypred : ndarray of length n_samples
            Predicted labels.
        """
        y_pred = self._predict(X)
        if self.n_outputs_ == 1:
            y_pred = y_pred.ravel()
        return self._label_binarizer.inverse_transform(y_pred)

    def predict_log_proba(self, X):
        """
        Log of probability estimates.
        
        Parameters
        ----------
        X : ndarray of shape (n_samples, n_features)
            Input data.
        
        Returns
        -------
        yprob : ndarray of shape (n_samples, n_outputs)
            The ith row and jth column holds the log-probability of the ith
            sample to the jth class
        """
        return np.log(self.predict_proba(X))

    def predict_proba(self, X):
        """
        Probability estimates.
        
        Parameters
        ----------
        X : ndarray of shape (n_samples, n_features)
            Input data.
        
        Returns
        -------
        yprob : ndarray of shape (n_samples, n_outputs)
            The ith row and jth column holds the probability of the ith sample
            to the jth class
        """
        y_pred = self._predict(X)
        if self.n_outputs_ == 1:
            y_pred = y_pred.ravel()
        if y_pred.ndim == 1:
            return np.vstack([1.0 - y_pred, y_pred]).transpose()
        else:
            return y_pred

    def score(self, X, y):
        """
        Compute accuracy score.
        
        Parameters
        ----------
        X : ndarray of shape (n_samples, n_features)
            Input data.
        y : ndarray of length n_samples
            Target values.
            
        Returns
        -------
        acc : scalar
            Accuracy of prediction.
        """
        return np.mean(self.predict(X) == y)

    @property
    def weights(self):
        """
        list of ndarray
        Neural network weights. The ith element holds the weighs for the
        layer i.
        """
        return [np.array(coefs[:, 1:].T) for coefs in self.coefs_]

    @property
    def biases(self):
        """
        list of ndarray
        Neural network biases. The ith element holds the biases for the
        layer i.
        """
        return [np.array(coefs[:, 0]) for coefs in self.coefs_]

    @property
    def flag(self):
        """
        int
        Stopping criterion:
            - -1, maximum number of iterations is reached.
            - 0, best individual position changes less than eps1.
            - 1, fitness is lower than threshold eps2.
            - 2, NoEffectAxis (only when solver = {'cmaes', 'vdcma'}).
            - 3, NoEffectCoord (only when solver = {'cmaes', 'vdcma'}).
            - 4, ConditionCov (only when solver = {'cmaes', 'vdcma'}).
            - 5, EqualFunValues (only when solver = {'cmaes', 'vdcma'}).
            - 6, TolXUp (only when solver = {'cmaes', 'vdcma'}).
            - 7, TolFun (only when solver = {'cmaes', 'vdcma'}).
            - 8, TolX (only when solver = {'cmaes', 'vdcma'}).
        """
        return self.flag_

    @property
    def n_iter(self):
        """
        int
        Number of iterations required to reach stopping criterion.
        """
        return self.n_iter_

    @property
    def n_eval(self):
        """
        int
        Number of function evaluations performed.
        """
        return self.n_eval_