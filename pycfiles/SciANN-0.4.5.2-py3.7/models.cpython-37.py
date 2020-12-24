# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sciann/engine~/models.py
# Compiled at: 2020-03-20 20:49:57
# Size of source mod 2**32: 10937 bytes
""" SciModel class to define and train the model.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from ..utils import *
from keras.models import Model
from keras.utils import plot_model
from .functional import Variable, RadialBasisVariable
from constraints.constraint import Constraint

class SciModel(object):
    __doc__ = 'Configures the model for training.\n\n    # Arguments\n        inputs: Main variables (also called inputs, or independent variables) of the network, `xs`.\n            They all should be of type `Variable`.\n\n        targets: list all targets (also called outputs, or dependent variables)\n            to be satisfied during the training. Expected list members are:\n            - Entries of type `Constraint`, such as Data, Tie, etc.\n            - Entries of type `Functional` can be:\n                . A single `Functional`: will be treated as a zero constraint.\n                    An example is a PDE that is supposed to be zero.\n                . A tuple of (`Functional`, data: np.ndarray): will be treated as a `Constraint` of type `Data`.\n                . A tuple of (`Functional`, `Functional`): will be treated as a `Constraint` of type `Tie`.\n            - If you need to impose more complex types of constraints or\n                to impose a constraint partially in a specific part of region,\n                use `Data` or `Tie` classes from `Constraint`.\n\n        plot_to_file: A string file name to output the network architecture.\n\n    # Raises\n        ValueError: `inputs` must be of type Variable.\n                    `targets` must be of types `Functional`, or (`Functional`, data), or (`Functional`, `Functional`).\n    '

    def __init__(self, inputs=None, targets=None, loss_func='mse', plot_to_file=None, **kwargs):
        inputs = to_list(inputs)
        if not all([isinstance(x, (Variable, RadialBasisVariable)) for x in inputs]):
            raise ValueError('Please provide a `list` of `Variable` or `RadialBasisVariable` objects for inputs. ')
        else:
            input_vars = []
            for var in inputs:
                input_vars += var.inputs

            if targets is None:
                if 'constraints' in kwargs:
                    targets = kwargs.get('constraints')
                elif 'conditions' in kwargs:
                    targets = kwargs.get('conditions')
            elif 'conditions' in kwargs or 'constraints' in kwargs:
                raise TypeError('Inconsistent inputs: `constraints`, `conditions`, and `targets` are all equivalent keywords - pass all targets as a list to `SciModel`. ')
        targets = to_list(targets)
        if not all([isinstance(y, Constraint) for y in targets]):
            raise ValueError('Please provide a "list" of "Constraint"s.')
        output_vars = []
        for cond in targets:
            output_vars += cond().outputs

        if isinstance(loss_func, str) and loss_func in ('mse', 'mae'):
            loss_func = SciModel.loss_functions(loss_func)
        else:
            if not callable(loss_func):
                raise TypeError('Please provide a valid loss function from ("mse", "mae") or a callable function for input of tensor types. ')
        model = Model(inputs=input_vars, 
         outputs=output_vars, **kwargs)
        model.compile(loss=loss_func,
          optimizer='adam')
        self._model = model
        self._inputs = inputs
        self._constraints = targets
        self._loss_func = loss_func
        if plot_to_file is not None:
            plot_model((self._model), to_file=plot_to_file)

    @property
    def model(self):
        return self._model

    @property
    def constraints(self):
        return self._constraints

    @property
    def inputs(self):
        return self._inputs

    def verify_update_constraints(self, constraints):
        ver = []
        for old, new in zip(self._constraints, constraints):
            if old == new and old.sol == new.sol:
                if old.sol is None:
                    ver.append(True)
                elif all([all(xo == xn) for xo, xn in zip(old.sol, new.sol)]):
                    ver.append(True)
                else:
                    ver.append(False)
            else:
                ver.append(False)

        return all(ver)

    def __call__(self, *args, **kwargs):
        output = (self._model.__call__)(*args, **kwargs)
        if isinstance(output, list):
            return output
        return [output]

    def save(self, filepath, *args, **kwargs):
        return (self._model.save)(filepath, *args, **kwargs)

    def summary(self, *args, **kwargs):
        return (self._model.summary)(*args, **kwargs)

    def solve(self, x_true, weights=None, epochs=10, batch_size=256, shuffle=True, callbacks=None, stop_after=100, default_zero_weight=1e-10, **kwargs):
        """Performs the training on the model.

        # Arguments
            epochs: Integer. Number of epochs to train the model.
                An epoch is an iteration over the entire `x` and `y`
                data provided.
            batch_size: Integer or 'None'.
                Number of samples per gradient update.
                If unspecified, 'batch_size' will default to 128.
            shuffle: Boolean (whether to shuffle the training data).
                Default value is True.
            callbacks: List of `keras.callbacks.Callback` instances.

        # Returns
            A 'History' object after performing fitting.
        """
        if callbacks is None:
            callbacks = [
             k.callbacks.EarlyStopping(monitor='loss',
               mode='min',
               verbose=1,
               patience=stop_after),
             k.callbacks.TerminateOnNaN()]
        else:
            x_true = [x.reshape(-1, 1) if len(x.shape) == 1 else x for x in to_list(x_true)]
            num_sample = x_true[0].shape[0]
            assert all([x.shape[0] == num_sample for x in x_true[1:]])
            ids_all = np.arange(0, num_sample)
            if weights is None:
                weights = np.ones(num_sample)
            else:
                if len(weights.shape) != 1 or weights.shape[0] != num_sample:
                    raise ValueError('Input error: `weights` should have dimension 1 with the same sample length as `Xs. ')
        y_true, sample_weights = [], []
        for c in self._constraints:
            if c.ids is None:
                ids = ids_all
                wei = [weights for yi in c.cond.outputs]
            else:
                ids = c.ids
                wei = [np.zeros(num_sample) + default_zero_weight for yi in c.cond.outputs]
                for w in wei:
                    w[ids] = weights[ids]
                    w[ids] *= sum(weights) / sum(w[ids])

            sol = [np.zeros((num_sample,) + k.backend.int_shape(yi)[1:]) for yi in c.cond.outputs]
            if c.sol is not None:
                for yi, soli in zip(sol, c.sol):
                    yi[ids, :] = soli

            y_true += sol
            sample_weights += wei

        history = (self._model.fit)(
 x_true, y_true, sample_weight=sample_weights, 
         epochs=epochs, 
         batch_size=batch_size, 
         shuffle=shuffle, 
         callbacks=callbacks, **kwargs)
        return history

    def predict(self, x, batch_size=None, verbose=0, steps=None):
        """ Predict output from network.

        # Arguments
            x:
            batch_size:
            verbose:
            steps:

        # Returns
            List of numpy array of the size of network outputs.

        # Raises

        """
        return self._model.predict(x, batch_size, verbose, steps)

    def eval(self, *args):
        if len(args) == 1:
            x_data = to_list(args[0])
            if not all([isinstance(xi, np.ndarray) for xi in x_data]):
                raise ValueError('Please provide input data to the network. ')
            return unpack_singleton(self.predict(x_data))
        if len(args) == 2:
            var_name = args[0]
            if not isinstance(var_name, str):
                raise ValueError('Value Error: Expected a LayerName as the input. ')
            x_data = to_list(args[1])
            new_model = Model(self.inputs, self.get_layer(var_name).output)
            if not all([isinstance(xi, np.ndarray) for xi in x_data]):
                raise ValueError('Please provide input data to the network. ')
            return unpack_singleton(new_model.predict(x_data))

    def plot_model(self, *args, **kwargs):
        """ Keras plot_model functionality.
            Refer to Keras documentation for help.
        """
        plot_model(self._model, *args, **kwargs)

    @staticmethod
    def loss_functions(method='mse'):
        """ loss_function returns the callable object to evaluate the loss.

        # Arguments
            method: String.
                "mse" for `Mean Squared Error` or
                "mae" for 'Mean Absolute Error'.
        # Returns
            Callable function that gets (y_true, y_pred) as the input and
                returns the loss value as the output.
        # Raises
            ValueError if anything other than "mse" or "mae" is passed.
        """
        if method == 'mse':
            return lambda y_true, y_pred: K.mean(K.square(y_true - y_pred))
        if method == 'mae':
            return lambda y_true, y_pred: K.mean(K.abs(y_true - y_pred))
        raise ValueError