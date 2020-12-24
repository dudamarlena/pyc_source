# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/network/messenger/onion.py
# Compiled at: 2017-10-28 15:44:59
# Size of source mod 2**32: 3607 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
from wasp_general.verify import verify_type
from wasp_general.network.messenger.proto import WMessengerOnionProto
from wasp_general.network.messenger.proto import WMessengerOnionLayerProto
from wasp_general.network.messenger.layers import WMessengerSimpleCastingLayer
from wasp_general.network.messenger.coders import WMessengerFixedModificationLayer, WMessengerEncodingLayer
from wasp_general.network.messenger.coders import WMessengerHexLayer, WMessengerBase64Layer, WMessengerAESLayer
from wasp_general.network.messenger.coders import WMessengerRSALayer
from wasp_general.network.messenger.packers import WMessengerJSONPacker
from wasp_general.network.messenger.composer import WMessengerComposerLayer
from wasp_general.network.messenger.transport import WMessengerSendAgentLayer, WMessengerSyncReceiveAgentLayer

class WMessengerOnion(WMessengerOnionProto):
    __doc__ = ' :class:`.WMessengerOnionProto` implementation. This class holds layers\n\t(:class:`WMessengerOnionLayerProto` class) that can be used for message processing.\n\t'
    __builtin_layers__ = {x.name():x for x in [
     WMessengerFixedModificationLayer(), WMessengerEncodingLayer(), WMessengerHexLayer(),
     WMessengerBase64Layer(), WMessengerAESLayer(), WMessengerRSALayer(), WMessengerJSONPacker(),
     WMessengerSendAgentLayer(), WMessengerSyncReceiveAgentLayer(), WMessengerComposerLayer(),
     WMessengerSimpleCastingLayer()]}

    @verify_type(layers=WMessengerOnionLayerProto)
    def __init__(self, *layers):
        """ Construct new onion

                :param layers: layers to store
                """
        self._WMessengerOnion__layers = {}
        self.add_layers(*layers)

    def layers_names(self):
        """ :meth:`.WMessengerOnionProto.layer_names` method implementation.
                """
        return list(self.__class__.__builtin_layers__.keys()) + list(self._WMessengerOnion__layers.keys())

    @verify_type(layer_name=str)
    def layer(self, layer_name):
        """ :meth:`.WMessengerOnionProto.layer` method implementation.
                """
        if layer_name in self._WMessengerOnion__layers.keys():
            return self._WMessengerOnion__layers[layer_name]
        if layer_name in self.__class__.__builtin_layers__:
            return self.__class__.__builtin_layers__[layer_name]
        raise RuntimeError('Invalid layer name')

    @verify_type(layer=WMessengerOnionLayerProto)
    def add_layers(self, *layers):
        """ Append given layers to this onion

                :param layers: layer to add
                :return: None
                """
        for layer in layers:
            if layer.name() in self._WMessengerOnion__layers.keys():
                raise ValueError('Layer "%s" already exists' % layer.name())
            self._WMessengerOnion__layers[layer.name()] = layer