# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sciann/functionals/rnn_functional.py
# Compiled at: 2020-04-12 04:31:19
# Size of source mod 2**32: 10737 bytes
""" Functional class for SciANN.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import keras.backend as K
from keras.layers import Dense, LSTM, SimpleRNN
from keras.layers import Activation
from keras.layers import Concatenate
from ..utils import default_bias_initializer, default_kernel_initializer
from ..utils import to_list, unpack_singleton, get_activation
from ..utils import validations
from ..utils import math
from .rnn_field import RNNField

class RNNFunctional(object):
    __doc__ = " Configures the LSTMFunctional object (Recurrent Neural Network).\n\n    # Arguments\n        fields: String or Field.\n            [Sub-]Network outputs.\n            It can be of type `String` - Associated fields will be created internally.\n            It can be of type `Field` or `Functional`\n        variables: Variable.\n            [Sub-]Network inputs.\n            It can be of type `Variable` or other Functional objects.\n        hidden_layers: A list indicating neurons in the hidden layers.\n            e.g. [10, 100, 20] is a for hidden layers with 10, 100, 20, respectively.\n        rnn_type: currently, `SimpleRNN` and `LSTM` are accepted.\n            Defaulted to `SimpleRNN`.\n            Check `Keras` documentation for additional information.\n        activation: Activation function for the hidden layers.\n            Last layer will have a linear output.\n        enrichment: Activation function to be applied to the network output.\n        kernel_initializer: Initializer of the `Kernel`, from `k.initializers`.\n        bias_initializer: Initializer of the `Bias`, from `k.initializers`.\n        dtype: data-type of the network parameters, can be\n            ('float16', 'float32', 'float64').\n            Note: Only network inputs should be set.\n        trainable: Boolean.\n            False if network is not trainable, True otherwise.\n            Default value is True.\n\n    # Raises\n        ValueError:\n        TypeError:\n    "

    def __init__(self, fields=None, variables=None, hidden_layers=None, rnn_type='SimpleRNN', activation='tanh', recurrent_activation=None, enrichment='linear', kernel_initializer=default_kernel_initializer(), bias_initializer=default_bias_initializer(), dtype=None, trainable=True, **kwargs):
        if dtype is None:
            dtype = K.floatx()
        else:
            if not K.floatx() == dtype:
                K.set_floatx(dtype)
            elif all([x in kwargs for x in ('inputs', 'outputs', 'layers')]):
                self._inputs = kwargs['inputs'].copy()
                self._outputs = kwargs['outputs'].copy()
                self._layers = kwargs['layers'].copy()
                return
                fields = to_list(fields)
                if all([isinstance(fld, str) for fld in fields]):
                    outputs = [RNNField(name=fld, dtype=dtype, kernel_initializer=kernel_initializer, bias_initializer=bias_initializer, trainable=trainable) for fld in fields]
                else:
                    if all([validations.is_field(fld) for fld in fields]):
                        outputs = fields
                    else:
                        raise TypeError('Please provide a "list" of field names of type "String" or "Field" objects.')
                inputs = []
                layers = []
                variables = to_list(variables)
                if all([isinstance(var, RNNFunctional) for var in variables]):
                    for var in variables:
                        inputs += var.outputs

                    for var in variables:
                        for lay in var.layers:
                            layers.append(lay)

                else:
                    raise TypeError('Input error: Please provide a `list` of `Functional`s. \nProvided - {}'.format(variables))
                if hidden_layers is None:
                    hidden_layers = []
                else:
                    hidden_layers = to_list(hidden_layers)
                if isinstance(activation, list):
                    raise AssertionError('Expected an activation function name not a "list". ')
                afunc = get_activation(activation)
                enrichment = to_list(enrichment)
                efuncs = get_activation(enrichment)
                if len(inputs) == 1:
                    net_input = inputs[0]
            else:
                layer = Concatenate()
                layer.name = 'conct_' + layer.name.split('_')[(-1)]
                net_input = layer(inputs)
            net = []
            for enrich in efuncs:
                net.append(net_input)
                for nLay, nNeuron in enumerate(hidden_layers):
                    if rnn_type == 'LSTM':
                        layer = LSTM(nNeuron,
                          return_sequences=True,
                          recurrent_activation=recurrent_activation,
                          kernel_initializer=kernel_initializer,
                          bias_initializer=bias_initializer,
                          trainable=trainable,
                          dtype=dtype,
                          unroll=True)
                    else:
                        if rnn_type == 'SimpleRNN':
                            layer = SimpleRNN(nNeuron,
                              return_sequences=True,
                              kernel_initializer=kernel_initializer,
                              bias_initializer=bias_initializer,
                              trainable=trainable,
                              dtype=dtype,
                              unroll=True)
                        else:
                            raise ValueError('Invalid entry for `rnn_type` -- accepts from (`SimpleRNN`, `LSTM`).')
                    layer.name = 'D{:d}b_'.format(nNeuron) + layer.name.split('_')[(-1)]
                    layers.append(layer)
                    net[-1] = layer(net[(-1)])
                    if nLay < len(hidden_layers) - 1 and afunc.__name__ != 'linear':
                        layer = Activation(afunc)
                        layer.name = '{}_'.format(afunc.__name__) + layer.name.split('_')[(-1)]
                        layers.append(layer)
                        net[-1] = layer(net[(-1)])

                if enrich.__name__ != 'linear':
                    layer = Activation(enrich)
                    layer.name = '{}_'.format(enrich.__name__) + layer.name.split('_')[(-1)]
                    layers.append(layer)
                    net[-1] = layer(net[(-1)])

            for out in outputs:
                layers.append(out)

            if len(net) == 1:
                net_output = net[0]
            else:
                layer = Concatenate()
                layer.name = 'conct_' + layer.name.split('_')[(-1)]
                net_output = layer(net)
            outputs = [out(net_output) for out in outputs]
            self._inputs = inputs
            self._outputs = outputs
            self._layers = layers

    def eval(self, model, mesh):
        assert validations.is_scimodel(model), 'Expected a SciModel object. '
        return unpack_singleton(K.function(model.model.inputs, self._outputs)(mesh))

    @property
    def layers(self):
        return self._layers

    @layers.setter
    def layers(self, value):
        self._layers = value

    @property
    def inputs(self):
        return self._inputs

    @inputs.setter
    def inputs(self, value):
        self._inputs = value

    @property
    def outputs(self):
        return self._outputs

    @outputs.setter
    def outputs(self, value):
        self._outputs = value

    def copy(self):
        return RNNFunctional(inputs=(self.inputs),
          outputs=(self.outputs),
          layers=(self.layers))

    def append_to_layers(self, layers):
        self.layers = self.layers + layers

    def append_to_inputs(self, inputs):
        self.inputs = self.inputs + inputs

    def append_to_outputs(self, outputs):
        self.outputs = self.outputs + outputs

    def set_trainable(self, val):
        if isinstance(val, bool):
            for l in self._layers:
                l.trainable = val

        else:
            raise ValueError('Expected a boolean value: True or False')

    def split(self):
        """ In the case of `Functional` with multiple outputs,
            you can split the outputs and get an associated functional.

        # Returns
            (f1, f2, ...): Tuple of splitted `Functional` objects
                associated to cheach outputs.
        """
        if len(self._outputs) == 1:
            return self
        fs = ()
        nr = len(self._outputs)
        lays = self.layers[:-nr]
        for out, lay in zip(self._outputs, self._layers[-nr:]):
            f = RNNFunctional(inputs=(to_list(self.inputs)),
              outputs=(to_list(out)),
              layers=(lays + to_list(lay)))
            fs += (f,)

        return fs

    def __call__(self):
        return self.outputs

    def __pos__(self):
        return self

    def __neg__(self):
        return self * -1.0

    def __add__(self, other):
        return math.add(self, other)

    def __radd__(self, other):
        return math.radd(self, other)

    def __sub__(self, other):
        return math.sub(self, other)

    def __rsub__(self, other):
        return math.rsub(self, other)

    def __mul__(self, other):
        return math.mul(self, other)

    def __rmul__(self, other):
        return math.rmul(self, other)

    def __truediv__(self, other):
        return math.div(self, other)

    def __rtruediv__(self, other):
        return math.rdiv(self, other)

    def __pow__(self, power):
        return math.pow(self, power)

    def diff(self, *args, **kwargs):
        return (math.diff)(self, *args, **kwargs)

    @classmethod
    def get_class(cls):
        return RNNFunctional