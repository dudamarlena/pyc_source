# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sciann/models/model.py
# Compiled at: 2020-04-21 18:18:57
# Size of source mod 2**32: 24408 bytes
""" SciModel class to define and train the model.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os
import keras.backend as K
import keras as k, numpy as np
from keras.models import Model
from keras.utils import plot_model
from ..utils import unpack_singleton, to_list
from ..utils import is_variable, is_constraint, is_functional
from ..functionals import Variable
from ..functionals import RadialBasis
from ..constraints import Data, Tie

class SciModel(object):
    __doc__ = 'Configures the model for training.\n    Example:\n    # Arguments\n        inputs: Main variables (also called inputs, or independent variables) of the network, `xs`.\n            They all should be of type `Variable`.\n        targets: list all targets (also called outputs, or dependent variables)\n            to be satisfied during the training. Expected list members are:\n            - Entries of type `Constraint`, such as Data, Tie, etc.\n            - Entries of type `Functional` can be:\n                . A single `Functional`: will be treated as a Data constraint.\n                    The object can be just a `Functional` or any derivatives of `Functional`s.\n                    An example is a PDE that is supposed to be zero.\n                . A tuple of (`Functional`, `Functional`): will be treated as a `Constraint` of type `Tie`.\n            - If you need to impose more complex types of constraints or\n                to impose a constraint partially in a specific part of region,\n                use `Data` or `Tie` classes from `Constraint`.\n        loss_func: defaulted to "mse" or "mean_squared_error".\n            It can be an string from supported loss functions, i.e. ("mse" or "mae").\n            Alternatively, you can create your own loss function and\n            pass the function handle (check Keras for more information).\n        optimizer: defaulted to "adam" optimizer.\n            It can be one of Keras accepted optimizers, e.g. "adam".\n            You can also pass more details on the optimizer:\n            - `optimizer = k.optimizers.RMSprop(lr=0.01, rho=0.9, epsilon=None, decay=0.0)`\n            - `optimizer = k.optimizers.SGD(lr=0.001, momentum=0.0, decay=0.0, nesterov=False)`\n            - `optimizer = k.optimizers.Adam(lr=0.01, beta_1=0.9, beta_2=0.999, epsilon=None, decay=0.0, amsgrad=False)`\n            Check our Keras documentation for further details. We have found\n        load_weights_from: (file_path) Instantiate state of the model from a previously saved state.\n        plot_to_file: A string file name to output the network architecture.\n\n    # Raises\n        ValueError: `inputs` must be of type Variable.\n                    `targets` must be of types `Functional`, or (`Functional`, data), or (`Functional`, `Functional`).\n    '

    def __init__(self, inputs=None, targets=None, loss_func='mse', optimizer='adam', load_weights_from=None, plot_to_file=None, **kwargs):
        inputs = to_list(inputs)
        if not all([is_variable(x) for x in inputs]):
            raise ValueError('Please provide a `list` of `Variable` or `RadialBasis` objects for inputs. ')
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
        for i, y in enumerate(targets):
            if not is_constraint(y):
                if is_functional(y):
                    targets[i] = Data(y)
                else:
                    if isinstance(y, tuple):
                        if len(y) == 2:
                            if is_functional(y[0]):
                                if is_functional(y[1]):
                                    targets[i] = Tie(y[0], y[1])
                    raise ValueError('The {}th target entry is not of type `Constraint` or `Functional` - received \n ++++++ {} '.format(i, y))

        output_vars = []
        for cond in targets:
            output_vars += cond().outputs

        if isinstance(loss_func, str):
            loss_func = SciModel.loss_functions(loss_func)
        else:
            if not callable(loss_func):
                raise TypeError('Please provide a valid loss function from ("mse", "mae") or a callable function for input of tensor types. ')
            else:
                model = Model(inputs=input_vars, 
                 outputs=output_vars, **kwargs)
                model.compile(loss=loss_func,
                  optimizer=optimizer)
                if load_weights_from is not None:
                    if os.path.exists(load_weights_from):
                        model.load_weights(load_weights_from)
                    else:
                        raise Warning('File not found - load_weights_from: {}'.format(load_weights_from))
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

    def save_weights(self, filepath, *args, **kwargs):
        return (self._model.save_weights)(filepath, *args, **kwargs)

    def load_weights(self, filepath, *args, **kwargs):
        return (self._model.load_weights)(filepath, *args, **kwargs)

    def summary(self, *args, **kwargs):
        return (self._model.summary)(*args, **kwargs)

    def train(self, x_true, y_true, weights=None, target_weights=None, batch_size=64, epochs=100, learning_rate=0.001, shuffle=True, callbacks=None, stop_after=None, save_weights_to=None, save_weights_freq=0, default_zero_weight=0.0, **kwargs):
        """Performs the training on the model.

        # Arguments
            x_true: list of `Xs` associated to targets of `Y`.
                Expecting a list of np.ndarray of size (N,1) each,
                with N as the sample size.
            y_true: list of true `Ys` associated to the targets defined during model setup.
                Expecting the same size as list of targets defined in `SciModel`.
                - To impose the targets at specific `Xs` only, pass a tuple of `(ids, y_true)` for that target.
            weights: (np.ndarray) A global sample weight to be applied to samples.
                Expecting an array of shape (N,1), with N as the sample size.
                Default value is `one` to consider all samples equally important.
            target_weights: (list) A weight for each target defined in `y_true`.
            batch_size: (Integer) or 'None'.
                Number of samples per gradient update.
                If unspecified, 'batch_size' will default to 2^6=64.
            epochs: (Integer) Number of epochs to train the model.
                Defaulted to 100.
                An epoch is an iteration over the entire `x` and `y`
                data provided.
            learning_rate: (Tuple/List) (epochs, lrs).
                Expects a list/tuple with a list of epochs and a list or learning rates.
                It linearly interpolates between entries.
                Defaulted to 0.001 with no decay.
                Example:
                    learning_rate = ([0, 100, 1000], [0.001, 0.0005, 0.00001])
            shuffle: Boolean (whether to shuffle the training data).
                Default value is True.
            callbacks: List of `keras.callbacks.Callback` instances.
            stop_after: To stop after certain missed epochs.
                Defaulted to epochs.
            save_weights_to: (file_path) If you want to save the state of the model (at the end of the training).
            save_weights_freq: (Integer) Save weights every N epcohs.
                Defaulted to 0.
            default_zero_weight: a small number for zero sample-weight.

        # Returns
            A Keras 'History' object after performing fitting.
        """
        if callbacks is None:
            callbacks = []
            if isinstance(learning_rate, (type(None), float, int)):
                lr_rates = 0.001 if learning_rate is None else learning_rate
                K.set_value(self.model.optimizer.lr, lr_rates)
                callbacks.append(k.callbacks.callbacks.ReduceLROnPlateau(monitor='loss',
                  factor=0.5,
                  patience=(epochs / 10),
                  cooldown=(epochs / 10),
                  verbose=1,
                  mode='auto',
                  min_delta=0.001,
                  min_lr=(0.001 * lr_rates)))
            else:
                if isinstance(learning_rate, (tuple, list)):
                    lr_epochs = learning_rate[0]
                    lr_rates = learning_rate[1]
                    callbacks.append(k.callbacks.LearningRateScheduler(lambda n: np.interp(n, lr_epochs, lr_rates)))
                else:
                    raise ValueError('learning rate: expecting a `float` or a tuple/list of two arrays with `epochs` and `learning rates`')
            if stop_after is None:
                stop_after = max([10, epochs / 10])
            callbacks += [
             k.callbacks.EarlyStopping(monitor='loss', mode='auto', verbose=1, patience=stop_after,
               min_delta=1e-12),
             k.callbacks.TerminateOnNaN()]
        x_true = to_list(x_true)
        for i, (x, xt) in enumerate(zip(x_true, self._model.inputs)):
            x_shape = tuple(xt.get_shape().as_list())
            if x.shape != x_shape:
                try:
                    x_true[i] = x.reshape((-1, ) + x_shape[1:])
                except:
                    print('Could not automatically convert the inputs to be of the same size as the expected input tensors. Please provide inputs of the same dimension as the `Variables`. ')
                    assert False

        num_sample = x_true[0].shape[0]
        assert all([x.shape[0] == num_sample for x in x_true[1:]]), 'Inconsistent sample size among `Xs`. '
        ids_all = np.arange(0, num_sample)
        if weights is None:
            weights = np.ones(num_sample)
        else:
            if not len(weights.shape) != 1:
                if weights.shape[0] != num_sample:
                    try:
                        weights = weights.reshape(num_sample)
                    except:
                        raise ValueError('Input error: `weights` should have dimension 1 with the same sample length as `Xs. ')

                y_true = to_list(y_true)
                assert len(y_true) == len(self._constraints), 'Miss-match between expected targets (constraints) defined in `SciModel` and the provided `y_true`s - expecting the same number of data points. '
                sample_weights, y_star = [], []
                for i, yt in enumerate(y_true):
                    c = self._constraints[i]
                    ys, wei = SciModel._prepare_data(c.cond.outputs, to_list(yt), weights, num_sample, default_zero_weight)
                    y_star += ys
                    sample_weights += wei

                if target_weights is not None:
                    if isinstance(target_weights, list):
                        if not len(target_weights) == len(y_true):
                            raise ValueError('Expected a list of weights for the same size as the targets - was provided {}'.format(target_weights))
                    else:
                        for i, cw in enumerate(target_weights):
                            sample_weights[i] *= cw

                model_file_path = None
                if save_weights_to is not None:
                    try:
                        self._model.save_weights('{}-start.hdf5'.format(save_weights_to))
                        model_file_path = save_weights_to + '-{epoch:05d}-{loss:.3e}.hdf5'
                        model_check_point = k.callbacks.callbacks.ModelCheckpoint(model_file_path,
                          monitor='loss', save_weights_only=True, mode='auto', period=(10 if save_weights_freq == 0 else save_weights_freq),
                          save_best_only=(True if save_weights_freq == 0 else False))
                    except:
                        print('\nWARNING: Failed to save model.weights to the provided path: {}\n'.format(save_weights_to))

                if model_file_path is not None:
                    callbacks.append(model_check_point)
            else:
                history = (self._model.fit)(
 x_true, y_star, sample_weight=sample_weights, 
                 epochs=epochs, 
                 batch_size=batch_size, 
                 shuffle=shuffle, 
                 callbacks=callbacks, **kwargs)
                if save_weights_to is not None:
                    try:
                        self._model.save_weights('{}-end.hdf5'.format(save_weights_to))
                    except:
                        print('\nWARNING: Failed to save model.weights to the provided path: {}\n'.format(save_weights_to))

            return history

    def predict(self, xs, batch_size=None, verbose=0, steps=None):
        """ Predict output from network.

        # Arguments
            xs: list of `Xs` associated model.
                Expecting a list of np.ndarray of size (N,1) each,
                with N as the sample size.
            batch_size: defaulted to None.
                Check Keras documentation for more information.
            verbose: defaulted to 0 (None).
                Check Keras documentation for more information.
            steps: defaulted to 0 (None).
                Check Keras documentation for more information.

        # Returns
            List of numpy array of the size of network outputs.

        # Raises
            ValueError if number of `xs`s is different from number of `inputs`.
        """
        xs = to_list(xs)
        if len(xs) != len(self._inputs):
            raise ValueError('Please provide consistent number of inputs as the model is defined: Expected {} - provided {}'.format(len(self._inputs), len(to_list(xs))))
        shape_default = xs[0].shape if all([x.shape == xs[0].shape for x in xs]) else None
        for i, (x, xt) in enumerate(zip(xs, self._model.inputs)):
            x_shape = tuple(xt.get_shape().as_list())
            if x.shape != x_shape:
                try:
                    xs[i] = x.reshape((-1, ) + x_shape[1:])
                except:
                    print('Could not automatically convert the inputs to be of the same size as the expected input tensors. Please provide inputs of the same dimension as the `Variables`. ')
                    assert False

        y_pred = self._model.predict(xs, batch_size, verbose, steps)
        if shape_default is not None:
            try:
                y_pred = [y.reshape(shape_default) for y in y_pred]
            except:
                print('Input and output dimensions need re-adjustment for post-processing.')

        return unpack_singleton(y_pred)

    def eval(self, *args):
        if len(args) == 1:
            x_data = to_list(args[0])
            if len(x_data) != len(self._inputs):
                raise ValueError('Please provide consistent number of inputs as the model is defined: Expected {} - provided {}'.format(len(self._inputs), len(x_data)))
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
            - "mse" for `Mean Squared Error` or
            - "mae" for `Mean Absolute Error` or
            - "se" for `Squared Error` or
            - "ae" for `Absolute Error`.

        # Returns
            Callable function that gets (y_true, y_pred) as the input and
                returns the loss value as the output.

        # Raises
            ValueError if anything other than "mse" or "mae" is passed.
        """
        if method in ('mse', 'mean_squared_error'):
            return lambda y_true, y_pred: K.mean((K.square(y_true - y_pred)), axis=(-1))
        if method in ('mae', 'mean_absolute_error'):
            return lambda y_true, y_pred: K.mean((K.abs(y_true - y_pred)), axis=(-1))
        if method in ('se', 'squared_error'):
            return lambda y_true, y_pred: K.sum((K.square(y_true - y_pred)), axis=(-1))
        if method in ('ae', 'absolute_error'):
            return lambda y_true, y_pred: K.sum((K.abs(y_true - y_pred)), axis=(-1))
        if hasattr(k.losses, method):
            return getattr(k.losses, method)
        raise ValueError('Supported losses: Keras loss function or (mse, mae, se, ae)')

    @staticmethod
    def _prepare_data--- This code section failed: ---

 L. 495         0  BUILD_LIST_0          0 
                2  BUILD_LIST_0          0 
                4  ROT_TWO          
                6  STORE_FAST               'ys'
                8  STORE_FAST               'weis'

 L. 496        10  LOAD_GLOBAL              np
               12  LOAD_METHOD              arange
               14  LOAD_CONST               0
               16  LOAD_FAST                'num_sample'
               18  CALL_METHOD_2         2  '2 positional arguments'
               20  STORE_FAST               'ids_all'

 L. 498     22_24  SETUP_LOOP          894  'to 894'
               26  LOAD_GLOBAL              enumerate
               28  LOAD_GLOBAL              to_list
               30  LOAD_FAST                'y_true'
               32  CALL_FUNCTION_1       1  '1 positional argument'
               34  CALL_FUNCTION_1       1  '1 positional argument'
               36  GET_ITER         
             38_0  COME_FROM           846  '846'
            38_40  FOR_ITER            892  'to 892'
               42  UNPACK_SEQUENCE_2     2 
               44  STORE_FAST               'i'
               46  STORE_FAST               'yt'

 L. 499        48  LOAD_CONST               None
               50  STORE_FAST               'ids'

 L. 500        52  LOAD_FAST                'cond_outputs'
               54  LOAD_FAST                'i'
               56  BINARY_SUBSCR    
               58  STORE_FAST               'yc'

 L. 501        60  LOAD_GLOBAL              isinstance
               62  LOAD_FAST                'yt'
               64  LOAD_GLOBAL              tuple
               66  CALL_FUNCTION_2       2  '2 positional arguments'
            68_70  POP_JUMP_IF_FALSE   258  'to 258'
               72  LOAD_GLOBAL              len
               74  LOAD_FAST                'yt'
               76  CALL_FUNCTION_1       1  '1 positional argument'
               78  LOAD_CONST               2
               80  COMPARE_OP               ==
            82_84  POP_JUMP_IF_FALSE   258  'to 258'

 L. 502        86  LOAD_FAST                'yt'
               88  LOAD_CONST               0
               90  BINARY_SUBSCR    
               92  LOAD_METHOD              flatten
               94  CALL_METHOD_0         0  '0 positional arguments'
               96  STORE_FAST               'ids'

 L. 503        98  LOAD_GLOBAL              isinstance
              100  LOAD_FAST                'yt'
              102  LOAD_CONST               1
              104  BINARY_SUBSCR    
              106  LOAD_GLOBAL              np
              108  LOAD_ATTR                ndarray
              110  CALL_FUNCTION_2       2  '2 positional arguments'
              112  POP_JUMP_IF_FALSE   238  'to 238'

 L. 504       114  LOAD_FAST                'yt'
              116  LOAD_CONST               1
              118  BINARY_SUBSCR    
              120  STORE_FAST               'adjusted_yt'

 L. 505       122  LOAD_FAST                'ids'
              124  LOAD_ATTR                size
              126  LOAD_FAST                'yt'
              128  LOAD_CONST               1
              130  BINARY_SUBSCR    
              132  LOAD_ATTR                shape
              134  LOAD_CONST               0
              136  BINARY_SUBSCR    
              138  COMPARE_OP               ==
              140  POP_JUMP_IF_FALSE   204  'to 204'
              142  LOAD_FAST                'ids'
              144  LOAD_ATTR                size
              146  LOAD_FAST                'num_sample'
              148  COMPARE_OP               <
              150  POP_JUMP_IF_FALSE   204  'to 204'

 L. 506       152  LOAD_GLOBAL              np
              154  LOAD_METHOD              zeros
              156  LOAD_FAST                'num_sample'
              158  BUILD_TUPLE_1         1 
              160  LOAD_FAST                'yt'
              162  LOAD_CONST               1
              164  BINARY_SUBSCR    
              166  LOAD_ATTR                shape
              168  LOAD_CONST               1
              170  LOAD_CONST               None
              172  BUILD_SLICE_2         2 
              174  BINARY_SUBSCR    
              176  BINARY_ADD       
              178  CALL_METHOD_1         1  '1 positional argument'
              180  STORE_FAST               'adjusted_yt'

 L. 507       182  LOAD_FAST                'yt'
              184  LOAD_CONST               1
              186  BINARY_SUBSCR    
              188  LOAD_FAST                'adjusted_yt'
              190  LOAD_FAST                'ids'
              192  LOAD_CONST               None
              194  LOAD_CONST               None
              196  BUILD_SLICE_2         2 
              198  BUILD_TUPLE_2         2 
              200  STORE_SUBSCR     
              202  JUMP_ABSOLUTE       246  'to 246'
            204_0  COME_FROM           150  '150'
            204_1  COME_FROM           140  '140'

 L. 508       204  LOAD_FAST                'yt'
              206  LOAD_CONST               1
              208  BINARY_SUBSCR    
              210  LOAD_ATTR                shape
              212  LOAD_CONST               0
              214  BINARY_SUBSCR    
              216  LOAD_FAST                'num_sample'
              218  COMPARE_OP               !=
              220  POP_JUMP_IF_FALSE   246  'to 246'

 L. 509       222  LOAD_GLOBAL              ValueError

 L. 510       224  LOAD_STR                 'Error in size of the target {}.'
              226  LOAD_METHOD              format
              228  LOAD_FAST                'i'
              230  CALL_METHOD_1         1  '1 positional argument'
              232  CALL_FUNCTION_1       1  '1 positional argument'
              234  RAISE_VARARGS_1       1  'exception instance'
              236  JUMP_FORWARD        246  'to 246'
            238_0  COME_FROM           112  '112'

 L. 513       238  LOAD_FAST                'yt'
              240  LOAD_CONST               1
              242  BINARY_SUBSCR    
              244  STORE_FAST               'adjusted_yt'
            246_0  COME_FROM           236  '236'
            246_1  COME_FROM           220  '220'

 L. 514       246  LOAD_FAST                'ys'
              248  LOAD_METHOD              append
              250  LOAD_FAST                'adjusted_yt'
              252  CALL_METHOD_1         1  '1 positional argument'
              254  POP_TOP          
              256  JUMP_FORWARD        306  'to 306'
            258_0  COME_FROM            82  '82'
            258_1  COME_FROM            68  '68'

 L. 515       258  LOAD_GLOBAL              isinstance
              260  LOAD_FAST                'yt'
              262  LOAD_GLOBAL              np
              264  LOAD_ATTR                ndarray
              266  LOAD_GLOBAL              str
              268  LOAD_GLOBAL              float
              270  LOAD_GLOBAL              int
              272  LOAD_GLOBAL              type
              274  LOAD_CONST               None
              276  CALL_FUNCTION_1       1  '1 positional argument'
              278  BUILD_TUPLE_5         5 
              280  CALL_FUNCTION_2       2  '2 positional arguments'
          282_284  POP_JUMP_IF_FALSE   298  'to 298'

 L. 516       286  LOAD_FAST                'ys'
              288  LOAD_METHOD              append
              290  LOAD_FAST                'yt'
              292  CALL_METHOD_1         1  '1 positional argument'
              294  POP_TOP          
              296  JUMP_FORWARD        306  'to 306'
            298_0  COME_FROM           282  '282'

 L. 518       298  LOAD_GLOBAL              ValueError

 L. 519       300  LOAD_STR                 'Unrecognized entry - please provide a list of `data` or tuples of `(ids, data)` for each target defined in `SciModel`. '
              302  CALL_FUNCTION_1       1  '1 positional argument'
              304  RAISE_VARARGS_1       1  'exception instance'
            306_0  COME_FROM           296  '296'
            306_1  COME_FROM           256  '256'

 L. 523       306  LOAD_FAST                'ids'
              308  LOAD_CONST               None
              310  COMPARE_OP               is
          312_314  POP_JUMP_IF_FALSE   326  'to 326'

 L. 524       316  LOAD_FAST                'ids_all'
              318  STORE_FAST               'ids'

 L. 525       320  LOAD_FAST                'global_weights'
              322  STORE_FAST               'wei'
              324  JUMP_FORWARD        384  'to 384'
            326_0  COME_FROM           312  '312'

 L. 527       326  LOAD_GLOBAL              np
              328  LOAD_METHOD              zeros
              330  LOAD_FAST                'num_sample'
              332  CALL_METHOD_1         1  '1 positional argument'
              334  LOAD_FAST                'default_zero_weight'
              336  BINARY_ADD       
              338  STORE_FAST               'wei'

 L. 528       340  LOAD_FAST                'global_weights'
              342  LOAD_FAST                'ids'
              344  BINARY_SUBSCR    
              346  LOAD_FAST                'wei'
              348  LOAD_FAST                'ids'
              350  STORE_SUBSCR     

 L. 529       352  LOAD_FAST                'wei'
              354  LOAD_FAST                'ids'
              356  DUP_TOP_TWO      
              358  BINARY_SUBSCR    
              360  LOAD_GLOBAL              sum
              362  LOAD_FAST                'global_weights'
              364  CALL_FUNCTION_1       1  '1 positional argument'
              366  LOAD_GLOBAL              sum
              368  LOAD_FAST                'wei'
              370  LOAD_FAST                'ids'
              372  BINARY_SUBSCR    
              374  CALL_FUNCTION_1       1  '1 positional argument'
              376  BINARY_TRUE_DIVIDE
              378  INPLACE_MULTIPLY 
              380  ROT_THREE        
              382  STORE_SUBSCR     
            384_0  COME_FROM           324  '324'

 L. 530       384  LOAD_FAST                'weis'
              386  LOAD_METHOD              append
              388  LOAD_FAST                'wei'
              390  CALL_METHOD_1         1  '1 positional argument'
              392  POP_TOP          

 L. 532       394  LOAD_GLOBAL              isinstance
              396  LOAD_FAST                'ys'
              398  LOAD_CONST               -1
              400  BINARY_SUBSCR    
              402  LOAD_GLOBAL              np
              404  LOAD_ATTR                ndarray
              406  CALL_FUNCTION_2       2  '2 positional arguments'
          408_410  POP_JUMP_IF_FALSE   534  'to 534'

 L. 533       412  LOAD_FAST                'ys'
              414  LOAD_CONST               -1
              416  BINARY_SUBSCR    
              418  LOAD_ATTR                shape
              420  LOAD_CONST               1
              422  LOAD_CONST               None
              424  BUILD_SLICE_2         2 
              426  BINARY_SUBSCR    
              428  LOAD_GLOBAL              k
              430  LOAD_ATTR                backend
              432  LOAD_METHOD              int_shape
              434  LOAD_FAST                'yc'
              436  CALL_METHOD_1         1  '1 positional argument'
              438  LOAD_CONST               1
              440  LOAD_CONST               None
              442  BUILD_SLICE_2         2 
              444  BINARY_SUBSCR    
              446  COMPARE_OP               ==
          448_450  POP_JUMP_IF_TRUE    838  'to 838'

 L. 534       452  SETUP_EXCEPT        496  'to 496'

 L. 535       454  LOAD_FAST                'ys'
              456  LOAD_CONST               -1
              458  BINARY_SUBSCR    
              460  LOAD_METHOD              reshape
              462  LOAD_CONST               (-1,)
              464  LOAD_GLOBAL              k
              466  LOAD_ATTR                backend
              468  LOAD_METHOD              int_shape
              470  LOAD_FAST                'yc'
              472  CALL_METHOD_1         1  '1 positional argument'
              474  LOAD_CONST               1
              476  LOAD_CONST               None
              478  BUILD_SLICE_2         2 
              480  BINARY_SUBSCR    
              482  BINARY_ADD       
              484  CALL_METHOD_1         1  '1 positional argument'
              486  LOAD_FAST                'ys'
              488  LOAD_CONST               -1
              490  STORE_SUBSCR     
              492  POP_BLOCK        
              494  JUMP_FORWARD        838  'to 838'
            496_0  COME_FROM_EXCEPT    452  '452'

 L. 536       496  DUP_TOP          
              498  LOAD_GLOBAL              ValueError
              500  LOAD_GLOBAL              TypeError
              502  BUILD_TUPLE_2         2 
              504  COMPARE_OP               exception-match
          506_508  POP_JUMP_IF_FALSE   528  'to 528'
              510  POP_TOP          
              512  POP_TOP          
              514  POP_TOP          

 L. 537       516  LOAD_GLOBAL              ValueError

 L. 538       518  LOAD_STR                 'Dimension of expected `y_true` does not match with defined `Constraint`'
              520  CALL_FUNCTION_1       1  '1 positional argument'
              522  RAISE_VARARGS_1       1  'exception instance'
              524  POP_EXCEPT       
              526  JUMP_FORWARD        838  'to 838'
            528_0  COME_FROM           506  '506'
              528  END_FINALLY      
          530_532  JUMP_FORWARD        838  'to 838'
            534_0  COME_FROM           408  '408'

 L. 540       534  LOAD_GLOBAL              isinstance
              536  LOAD_FAST                'ys'
              538  LOAD_CONST               -1
              540  BINARY_SUBSCR    
              542  LOAD_GLOBAL              str
              544  CALL_FUNCTION_2       2  '2 positional arguments'
          546_548  POP_JUMP_IF_FALSE   692  'to 692'

 L. 541       550  LOAD_FAST                'ys'
              552  LOAD_CONST               -1
              554  BINARY_SUBSCR    
              556  LOAD_STR                 'zero'
              558  COMPARE_OP               ==
          560_562  POP_JUMP_IF_TRUE    578  'to 578'
              564  LOAD_FAST                'ys'
              566  LOAD_CONST               -1
              568  BINARY_SUBSCR    
              570  LOAD_STR                 'zeros'
              572  COMPARE_OP               ==
          574_576  POP_JUMP_IF_FALSE   616  'to 616'
            578_0  COME_FROM           560  '560'

 L. 542       578  LOAD_GLOBAL              np
              580  LOAD_METHOD              zeros
              582  LOAD_FAST                'num_sample'
              584  BUILD_TUPLE_1         1 
              586  LOAD_GLOBAL              k
              588  LOAD_ATTR                backend
              590  LOAD_METHOD              int_shape
              592  LOAD_FAST                'yc'
              594  CALL_METHOD_1         1  '1 positional argument'
              596  LOAD_CONST               1
              598  LOAD_CONST               None
              600  BUILD_SLICE_2         2 
              602  BINARY_SUBSCR    
              604  BINARY_ADD       
              606  CALL_METHOD_1         1  '1 positional argument'
              608  LOAD_FAST                'ys'
              610  LOAD_CONST               -1
              612  STORE_SUBSCR     
              614  JUMP_FORWARD        690  'to 690'
            616_0  COME_FROM           574  '574'

 L. 543       616  LOAD_FAST                'ys'
              618  LOAD_CONST               -1
              620  BINARY_SUBSCR    
              622  LOAD_STR                 'one'
              624  COMPARE_OP               ==
          626_628  POP_JUMP_IF_TRUE    644  'to 644'
              630  LOAD_FAST                'ys'
              632  LOAD_CONST               -1
              634  BINARY_SUBSCR    
              636  LOAD_STR                 'ones'
              638  COMPARE_OP               ==
          640_642  POP_JUMP_IF_FALSE   682  'to 682'
            644_0  COME_FROM           626  '626'

 L. 544       644  LOAD_GLOBAL              np
              646  LOAD_METHOD              ones
              648  LOAD_FAST                'num_sample'
              650  BUILD_TUPLE_1         1 
              652  LOAD_GLOBAL              k
              654  LOAD_ATTR                backend
              656  LOAD_METHOD              int_shape
              658  LOAD_FAST                'yc'
              660  CALL_METHOD_1         1  '1 positional argument'
              662  LOAD_CONST               1
              664  LOAD_CONST               None
              666  BUILD_SLICE_2         2 
              668  BINARY_SUBSCR    
              670  BINARY_ADD       
              672  CALL_METHOD_1         1  '1 positional argument'
              674  LOAD_FAST                'ys'
              676  LOAD_CONST               -1
              678  STORE_SUBSCR     
              680  JUMP_FORWARD        690  'to 690'
            682_0  COME_FROM           640  '640'

 L. 546       682  LOAD_GLOBAL              ValueError

 L. 547       684  LOAD_STR                 'Unexpected `str` entry - only accepts `zeros` or `ones`.'
              686  CALL_FUNCTION_1       1  '1 positional argument'
              688  RAISE_VARARGS_1       1  'exception instance'
            690_0  COME_FROM           680  '680'
            690_1  COME_FROM           614  '614'
              690  JUMP_FORWARD        838  'to 838'
            692_0  COME_FROM           546  '546'

 L. 549       692  LOAD_GLOBAL              isinstance
              694  LOAD_FAST                'ys'
              696  LOAD_CONST               -1
              698  BINARY_SUBSCR    
              700  LOAD_GLOBAL              int
              702  LOAD_GLOBAL              float
              704  BUILD_TUPLE_2         2 
              706  CALL_FUNCTION_2       2  '2 positional arguments'
          708_710  POP_JUMP_IF_FALSE   762  'to 762'

 L. 550       712  LOAD_GLOBAL              np
              714  LOAD_METHOD              ones
              716  LOAD_FAST                'num_sample'
              718  BUILD_TUPLE_1         1 
              720  LOAD_GLOBAL              k
              722  LOAD_ATTR                backend
              724  LOAD_METHOD              int_shape
              726  LOAD_FAST                'yc'
              728  CALL_METHOD_1         1  '1 positional argument'
              730  LOAD_CONST               1
              732  LOAD_CONST               None
              734  BUILD_SLICE_2         2 
              736  BINARY_SUBSCR    
              738  BINARY_ADD       
              740  CALL_METHOD_1         1  '1 positional argument'
              742  LOAD_GLOBAL              float
              744  LOAD_FAST                'ys'
              746  LOAD_CONST               -1
              748  BINARY_SUBSCR    
              750  CALL_FUNCTION_1       1  '1 positional argument'
              752  BINARY_MULTIPLY  
              754  LOAD_FAST                'ys'
              756  LOAD_CONST               -1
              758  STORE_SUBSCR     
              760  JUMP_FORWARD        838  'to 838'
            762_0  COME_FROM           708  '708'

 L. 551       762  LOAD_GLOBAL              isinstance
              764  LOAD_FAST                'ys'
              766  LOAD_CONST               -1
              768  BINARY_SUBSCR    
              770  LOAD_GLOBAL              type
              772  LOAD_CONST               None
              774  CALL_FUNCTION_1       1  '1 positional argument'
              776  CALL_FUNCTION_2       2  '2 positional arguments'
          778_780  POP_JUMP_IF_FALSE   820  'to 820'

 L. 552       782  LOAD_GLOBAL              np
              784  LOAD_METHOD              zeros
              786  LOAD_FAST                'num_sample'
              788  BUILD_TUPLE_1         1 
              790  LOAD_GLOBAL              k
              792  LOAD_ATTR                backend
              794  LOAD_METHOD              int_shape
              796  LOAD_FAST                'yc'
              798  CALL_METHOD_1         1  '1 positional argument'
            800_0  COME_FROM           494  '494'
              800  LOAD_CONST               1
              802  LOAD_CONST               None
              804  BUILD_SLICE_2         2 
              806  BINARY_SUBSCR    
              808  BINARY_ADD       
              810  CALL_METHOD_1         1  '1 positional argument'
              812  LOAD_FAST                'ys'
              814  LOAD_CONST               -1
              816  STORE_SUBSCR     
              818  JUMP_FORWARD        838  'to 838'
            820_0  COME_FROM           778  '778'

 L. 554       820  LOAD_GLOBAL              ValueError

 L. 555       822  LOAD_STR                 'Unsupported entry - {} '
              824  LOAD_METHOD              format
              826  LOAD_FAST                'ys'
              828  LOAD_CONST               -1
              830  BINARY_SUBSCR    
            832_0  COME_FROM           526  '526'
              832  CALL_METHOD_1         1  '1 positional argument'
              834  CALL_FUNCTION_1       1  '1 positional argument'
              836  RAISE_VARARGS_1       1  'exception instance'
            838_0  COME_FROM           818  '818'
            838_1  COME_FROM           760  '760'
            838_2  COME_FROM           690  '690'
            838_3  COME_FROM           530  '530'
            838_4  COME_FROM           448  '448'

 L. 558       838  LOAD_FAST                'ids'
              840  LOAD_ATTR                size
              842  LOAD_FAST                'num_sample'
              844  COMPARE_OP               !=
              846  POP_JUMP_IF_FALSE    38  'to 38'

 L. 559       848  LOAD_GLOBAL              np
              850  LOAD_ATTR                ones
              852  LOAD_FAST                'num_sample'
              854  LOAD_GLOBAL              bool
              856  LOAD_CONST               ('dtype',)
              858  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              860  STORE_FAST               'adjusted_ids'

 L. 560       862  LOAD_CONST               False
              864  LOAD_FAST                'adjusted_ids'
              866  LOAD_FAST                'ids'
              868  STORE_SUBSCR     

 L. 561       870  LOAD_CONST               0.0
              872  LOAD_FAST                'ys'
              874  LOAD_CONST               -1
              876  BINARY_SUBSCR    
              878  LOAD_FAST                'adjusted_ids'
              880  LOAD_CONST               None
              882  LOAD_CONST               None
              884  BUILD_SLICE_2         2 
              886  BUILD_TUPLE_2         2 
              888  STORE_SUBSCR     
              890  JUMP_BACK            38  'to 38'
              892  POP_BLOCK        
            894_0  COME_FROM_LOOP       22  '22'

 L. 563       894  LOAD_FAST                'ys'
              896  LOAD_FAST                'weis'
              898  BUILD_TUPLE_2         2 
              900  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM' instruction at offset 800_0