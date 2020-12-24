# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sciann/functionals/radialbasis.py
# Compiled at: 2020-04-12 04:32:12
# Size of source mod 2**32: 3304 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import keras.backend as K
from keras.layers import InputLayer
from ..utils import to_list
from ..utils import Lambda
from .functional import Functional
from .variable import Variable

class RadialBasis(Functional):
    __doc__ = ' Radial Basis functional class.\n    '

    def __init__(self, vars, rb_vars, radii):
        vars = to_list(vars)
        if not all([isinstance(x, Variable) for x in vars]):
            raise TypeError
        rb_vars = to_list(rb_vars)
        if not all([isinstance(x, RadialBasisBase) for x in rb_vars]):
            try:
                for i, rbv in enumerate(rb_vars):
                    rb_vars[i] = RadialBasisBase(rbv)

            except (ValueError, TypeError):
                raise ValueError('Expected `str` or `RadialBasisBase` as rb_vars. ')

        if len(vars) != len(rb_vars):
            raise ValueError
        if radii <= 0.0:
            raise ValueError('Expecting a positive value for `radii`. ')
        inputs, layers = [], []
        for v in vars:
            inputs += v.outputs
            layers += v.layers

        for v in rb_vars:
            inputs += v.outputs
            layers += v.layers

        lmbd = [Lambda(lambda x: K.exp(-(x[1] - x[0]) ** 2 / radii ** 2)) for i in range(len(vars))]
        outputs = []
        for i, l in enumerate(lmbd):
            l.name = '{}/'.format('RadialBasis') + l.name.split('_')[(-1)]
            assert len(vars[i].outputs) == 1
            assert len(rb_vars[i].outputs) == 1
            layers.append(l)
            outputs.append(l(vars[i].outputs + rb_vars[i].outputs))

        super(RadialBasis, self).__init__(layers=layers,
          inputs=inputs,
          outputs=outputs)

    @classmethod
    def get_class(cls):
        return Functional


class RadialBasisBase(Functional):
    __doc__ = " Configures the `RadialBasisBase` object for the network's input.\n\n    # Arguments\n        name: String.\n            Required as derivatives work only with layer names.\n        units (Int): Number of nodes to the network.\n            Minimum number is 1.\n        tensor: Tensorflow `Tensor`.\n            Can be pass as the input path.\n        dtype: data-type of the network parameters, can be\n            ('float16', 'float32', 'float64').\n\n    # Raises\n        ValueError: Provide `units > 0`.\n    "

    def __init__(self, name=None, units=1, tensor=None, dtype=None):
        if not dtype:
            dtype = K.floatx()
        else:
            if not dtype == K.floatx():
                K.set_floatx(dtype)
        if units < 1:
            raise ValueError('Expected at least one unit size - was provided `units`={:d}'.format(units))
        layer = InputLayer(batch_input_shape=(
         None, units),
          input_tensor=tensor,
          name=name,
          dtype=dtype)
        super(RadialBasisBase, self).__init__(layers=(to_list(layer)),
          inputs=(to_list(layer.input)),
          outputs=(to_list(layer.output)))

    @classmethod
    def get_class(cls):
        return Functional