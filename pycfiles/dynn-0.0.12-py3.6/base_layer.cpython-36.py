# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\dynn\layers\base_layer.py
# Compiled at: 2018-09-12 14:52:04
# Size of source mod 2**32: 620 bytes
"""
Base layer
==========
"""

class BaseLayer(object):
    __doc__ = 'Base layer interface'

    def __init__(self, pc, name):
        """Creates a subcollection for this layer with a custom name"""
        self.pc = pc.add_subcollection(name=name)

    def init(self, *args, **kwargs):
        """Initialize the layer before performing computation

        For example setup dropout, freeze some parameters, etc...
        """
        raise NotImplementedError()

    def __call__(self, *args, **kwargs):
        """Execute forward pass"""
        raise NotImplementedError()