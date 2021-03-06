# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/apogee/factors/discrete/factor.py
# Compiled at: 2019-06-30 07:13:00
# Size of source mod 2**32: 9286 bytes
import numpy as np, apogee as ap
from apogee.factors.base import Factor
from .operations import *
from .operations import factor_product, factor_division, factor_marginalise, factor_maximise, factor_reduce, factor_sum
from .optimise import maximum_likelihood_update

class DiscreteFactor(Factor):

    def __init__(self, scope, cardinality, parameters=None, alpha=0.0, samples=0, **kwargs):
        """
        A class representing a discrete stochastic factor.

        Parameters
        ----------
        scope: array_like, integer
            An array of integers corresponding to the variables in the scope of the current factor.
            Note that the ordering of this array is important -- make sure the scope mapping is
            correct!
        cardinality: array_like, integer
            An array of integers corresponding to the cardinality (number of states) of each of the
            variable in the scope of the factor. Once again, note that the order of this array should
            align exactly with the 'scope' array.
        parameters: array_like, float
            An array of floating point numbers representing the distribution of the factor. The
            factor expects to receive these parameters in log-space. Set the transform keyword to
            apply a transform to the parameters.
        alpha: float
            A prior, currently a fixed value, to be applied when fitting the factor to a dataset.
            Intuitively, this acts as

        References
        ----------
        D. Koller, N. Freidman: Probabilistic Graphical Models, Principles and Techniques
        F. Jensen: Bayesian Networks

        """
        super(DiscreteFactor, self).__init__(scope)
        self._samples = samples
        self._alpha = alpha
        self._cardinality = self._init_cards(cardinality)
        self._parameters = (self._init_params)(parameters, **kwargs)

    def fit(self, x: np.ndarray, y: np.ndarray=None):
        return self.fit_partial(x, y)

    def fit_partial(self, x: np.ndarray, y: np.ndarray=None):
        if y is not None:
            x = np.c_[(y, x)]
        self._parameters = maximum_likelihood_update(x,
          (self.assignments), parameters=(self.p), alpha=(self._alpha), n=(self._samples))
        self._samples += x.shape[0]
        return self

    def predict(self, x: np.ndarray):
        output = []
        for i, z in enumerate(x):
            evidence = [[self.scope[j], z[(j - 1)]] for j in range(1, self.scope[1:].shape[0] + 1)]
            output.append(((self.reduce)(*evidence, **{'inplace': False}).marginalise)(*[e[0] for e in evidence]).argmax())

        return np.asarray(output)

    def sum(self, *others, **kwargs):
        return (self._operation)(others, factor_sum, **kwargs)

    def product(self, *others, **kwargs):
        return (self._operation)(others, factor_product, **kwargs)

    def division(self, *others, **kwargs):
        return (self._operation)(others, factor_division, **kwargs)

    def normalise(self, inplace=False, row_wise=True, **kwargs):
        if row_wise:
            values = (self._row_wise_scaling)(**kwargs)
        else:
            values = (self._scaling)(**kwargs)
        if inplace:
            self._parameters = values
            return self
        else:
            return DiscreteFactor(self.scope, self.cards, values)

    def maximise(self, *others, **kwargs):
        return (self._operation)(others, factor_maximise, **kwargs)

    def marginalise(self, *others, **kwargs):
        return (self._operation)(others, factor_marginalise, **kwargs)

    def reduce(self, *evidence, **kwargs):
        return (self._operation)(evidence, factor_reduce, **kwargs)

    def mpe(self, mode='max', **kwargs):
        if mode == 'min':
            return self.assignments[(self.argmin)(**kwargs)]
        else:
            return self.assignments[(self.argmax)(**kwargs)]

    def max(self, **kwargs):
        return (np.max)((self.parameters), **kwargs)

    def min(self, **kwargs):
        return (np.min)((self.parameters), **kwargs)

    def argmax(self, **kwargs):
        return (np.argmax)((self.parameters), **kwargs)

    def argmin(self, **kwargs):
        return (np.argmin)((self.parameters), **kwargs)

    def log(self, inplace: bool=True, clip: float=1e-06):
        parameters = np.log(np.clip(self._parameters.copy(), clip))
        if inplace:
            self._parameters = parameters
            return self
        else:
            return DiscreteFactor(self.scope, self.cards, parameters)

    def exp(self, inplace: bool=True):
        parameters = np.exp(self._parameters.copy())
        if inplace:
            self._parameters = parameters
            return self
        else:
            return DiscreteFactor(self.scope, self.cards, parameters)

    def card(self, variable: int):
        return self.cards[ap.array_mapping(self.scope, [variable])]

    def subset(self, scope: np.ndarray):
        cards = [self.card(x)[0] for x in scope]
        return DiscreteFactor(scope, cards).identity

    @property
    def entropy(self):
        return ap.entropy(self._parameters)

    def index(self, assignment):
        return assignment_to_index(np.atleast_1d(np.asarray(assignment, dtype=(np.int64))), self.cards)

    def vacuous(self, *args, c: float=1.0, **kwargs):
        return (type(self))(
         (self.scope), (self.cards), (c * np.ones_like(self.parameters)), **kwargs)

    def assignment(self, index):
        return index_to_assignment(index, self.cards)

    def _init_params(self, params: np.ndarray or None, callback: callable=None, fill: float=0.0):
        if params is None:
            _params = ones_like_card(self.cards) * fill
        else:
            _params = np.asarray(params, dtype=(np.float32))
            m, n = len(_params), np.product(self.cards)
        assert m == n
        if callback is None:
            return _params
        else:
            return callback(_params)

    @staticmethod
    def _init_cards(cards: np.ndarray or list):
        """Initialise and validate an array of cardinalities."""
        _cards = np.asarray(cards, dtype=(np.int32))
        if not np.all([x >= 1 for x in cards]):
            raise ValueError('Invalid variable cardinality found: all variables must have one or more states in a DiscreteFactor')
        return _cards

    def _scaling(self, epsilon: float=1e-16, **kwargs):
        """Scale the factor's parameters."""
        return (ap.normalise)(self.parameters.copy(), a_min=epsilon, **kwargs)

    def _row_wise_scaling(self, epsilon: float=1e-16):
        """Apply row-wise scaling to the factor's parameters."""
        values = self.parameters.copy()
        parent_states = (ap.cartesian_product)(*np.array([np.arange(x) for x in self.cards[1:]]))
        for parent_state in parent_states:
            idx = []
            row_sum = epsilon
            for state in np.arange(self.cards[0]):
                idx.append(self.index([state, *parent_state]))
                row_sum += values[idx[(-1)]]

            values[idx] /= row_sum

        return values

    def _update(self, factor: 'DiscreteFactor', *args):
        """
        Update the Factor's parameters to match those in the passed Factor object.

        Parameters
        ----------
        factor: BaseFactor-like
            The Factor for which the current Factor's parameters should be updated to reflect.

        """
        self.scope = factor.scope
        self.cards = factor.cards
        self.parameters = factor.parameters
        return self

    @property
    def k(self):
        """Get the number of variables in the factor."""
        return len(self.scope)

    @property
    def n(self):
        """Get the total number of parameters of the factor."""
        return len(self.parameters)

    @property
    def p(self):
        """Alias for `parameter` attribute."""
        return self.parameters

    @property
    def cards(self):
        """Alias for `cardinality` attribute."""
        return self._cardinality

    @cards.setter
    def cards(self, values: np.ndarray):
        self._cardinality = self._init_cards(values)

    @property
    def assignments(self):
        """Generate a list of the unique states of the factor."""
        return (ap.cartesian_product)(*[np.arange(n) for n in self.cards])

    @property
    def identity(self):
        """Generate the identity factor for the current factor."""
        return self.vacuous()

    @property
    def marginals(self):
        """Generate the marginalse for each variable in the factor's scope."""
        return [(self.marginalise)(*ap.difference1d(self.scope, [v])) for v in self.scope]

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, value):
        self._parameters = self._init_params(value)