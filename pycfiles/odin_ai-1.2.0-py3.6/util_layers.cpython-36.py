# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/odin/networks/util_layers.py
# Compiled at: 2019-08-27 09:10:14
# Size of source mod 2**32: 2126 bytes
from __future__ import absolute_import, division, print_function
from tensorflow.python.keras import Sequential
from tensorflow.python.keras.layers import Activation, Dense, Layer
from tensorflow.python.util.tf_export import keras_export
__all__ = [
 'Identity', 'Parallel']

class Identity(Layer):

    def __init__(self, name=None):
        super(Identity, self).__init__(name=name)
        self.supports_masking = True

    def call(self, inputs, training=None):
        return inputs

    def compute_output_shape(self, input_shape):
        return input_shape


@keras_export('keras.models.Sequential', 'keras.Sequential')
class Parallel(Sequential):
    __doc__ = ' Similar design to keras `Sequential` but simultanously applying\n  all the layer on the input and return all the results.\n\n  This layer is important for implementing multitask learning.\n  '

    def call(self, inputs, training=None, mask=None, **kwargs):
        if self._is_graph_network:
            if not self.built:
                self._init_graph_network((self.inputs), (self.outputs), name=(self.name))
            return super(Parallel, self).call(inputs, training=training, mask=mask)
        else:
            outputs = []
            for layer in self.layers:
                kw = {}
                argspec = self._layer_call_argspecs[layer].args
                if 'mask' in argspec:
                    kw['mask'] = mask
                if 'training' in argspec:
                    kw['training'] = training
                for k, v in kwargs.items():
                    if k in argspec:
                        kw[k] = v

                o = layer(inputs, **kw)
                outputs.append(o)

            return tuple(outputs)

    def compute_output_shape(self, input_shape):
        shape = []
        for layer in self.layers:
            shape.append(layer.compute_output_shape(input_shape))

        return tuple(shape)

    def compute_mask(self, inputs, mask):
        outputs = self.call(inputs, mask=mask)
        return [o._keras_mask for o in outputs]