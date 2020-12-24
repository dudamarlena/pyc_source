# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extenteten/invertible.py
# Compiled at: 2017-01-06 05:01:09
# Size of source mod 2**32: 862 bytes
import abc, functools
__all__ = [
 'Invertible', 'InvertibleNetwork']
_FORWARD = 'forward'
_BACKWARD = 'backward'

class Invertible(abc.ABC):

    @abc.abstractmethod
    def forward(self, x):
        return NotImplemented

    @abc.abstractmethod
    def backward(self, x):
        return NotImplemented


class InvertibleNetwork(Invertible):

    def __init__(self, *layers):
        assert all(isinstance(layer, Invertible) for layer in layers)
        self._layers = layers

    def forward(self, x):
        return self._reduce_layers(_FORWARD, x)

    def backward(self, x):
        return self._reduce_layers(_BACKWARD, x)

    def _reduce_layers(self, method, x):
        return functools.reduce(lambda x, layer: getattr(layer, method)(x), self._layers if method == _FORWARD else reversed(self._layers), x)