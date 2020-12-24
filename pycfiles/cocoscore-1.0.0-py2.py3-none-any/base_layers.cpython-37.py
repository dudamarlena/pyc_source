# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: d:\dev\cocos2020\cocos\layer\base_layers.py
# Compiled at: 2020-01-10 23:58:31
# Size of source mod 2**32: 4869 bytes
__doc__ = "Layer class and subclasses.\n\nLayers are typically thought as event handlers and / or as containers that help\nto organize the scene visuals or logic.\n\nThe transform_anchor is set by default to the window's center, which most of the\ntime provides the desired behavior on rotation and scale.\n\nBy default a layer will not listen to events, his `is_event_handler` must be set\nto True before the layer enters the stage to enable the automatic registering as\nevent handler.\n"
from __future__ import division, print_function, unicode_literals
__docformat__ = 'restructuredtext'
import cocos.director as director
from cocos import cocosnode
from cocos import scene
__all__ = [
 'Layer', 'MultiplexLayer']

class Layer(cocosnode.CocosNode):
    """Layer"""
    is_event_handler = False

    def __init__(self):
        super(Layer, self).__init__()
        self.scheduled_layer = False
        x, y = director.get_window_size()
        self.transform_anchor_x = x // 2
        self.transform_anchor_y = y // 2

    def on_enter(self):
        super(Layer, self).on_enter()
        if self.is_event_handler:
            director.window.push_handlers(self)

    def on_exit(self):
        super(Layer, self).on_exit()
        if self.is_event_handler:
            director.window.remove_handlers(self)


class MultiplexLayer(Layer):
    """MultiplexLayer"""

    def __init__(self, *layers):
        super(MultiplexLayer, self).__init__()
        self.layers = layers
        self.enabled_layer = 0
        self.add(self.layers[self.enabled_layer])

    def switch_to(self, layer_number):
        """Switches to another of the layers managed by this instance.

        Arguments:
            layer_number (int) :
                **Must** be a number between 0 and the (number of layers - 1).
                The running layer will receive an ``on_exit()`` call, and the
                new layer will receive an ``on_enter()`` call.

        Raises:
            Exception: layer_number was out of bound.
        """
        if layer_number < 0 or layer_number >= len(self.layers):
            raise Exception('Multiplexlayer: Invalid layer number')
        self.remove(self.layers[self.enabled_layer])
        self.enabled_layer = layer_number
        self.add(self.layers[self.enabled_layer])