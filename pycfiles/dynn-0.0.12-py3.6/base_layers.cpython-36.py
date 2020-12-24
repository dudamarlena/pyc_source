# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\dynn\layers\base_layers.py
# Compiled at: 2018-09-17 12:24:03
# Size of source mod 2**32: 1107 bytes
"""
Base layer
==========
"""

class BaseLayer(object):
    __doc__ = 'Base layer interface'

    def __init__(self, name):
        self.name = name

    def init(self, *args, **kwargs):
        """Initialize the layer before performing computation

        For example setup dropout, freeze some parameters, etc...
        """
        pass

    def __call__(self, *args, **kwargs):
        """Execute forward pass"""
        raise NotImplementedError()


class ParametrizedLayer(BaseLayer):
    __doc__ = 'This is the base class for layers with trainable parameters'

    def __init__(self, pc, name):
        super(ParametrizedLayer, self).__init__(name)
        self.pc = pc.add_subcollection(name=name)

    def init(self, *args, **kwargs):
        """Initialize the layer before performing computation

        For example setup dropout, freeze some parameters, etc...
        This needs to be implemented for parametrized layers
        """
        raise NotImplementedError()