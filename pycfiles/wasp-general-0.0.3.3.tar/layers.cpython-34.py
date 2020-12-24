# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/network/messenger/layers.py
# Compiled at: 2018-04-15 05:02:21
# Size of source mod 2**32: 7570 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
from abc import abstractmethod
from enum import Enum
from wasp_general.verify import verify_type, verify_subclass
from wasp_general.network.messenger.proto import WMessengerEnvelopeProto
from wasp_general.network.messenger.proto import WMessengerOnionSessionProto, WMessengerOnionLayerProto
from wasp_general.network.messenger.envelope import WMessengerTextEnvelope, WMessengerBytesEnvelope

class WMessengerSimpleCastingLayer(WMessengerOnionLayerProto):
    __layer_name__ = 'com.binblob.wasp-general.simple-casting-layer'

    def __init__(self):
        """ Construct new layer
                """
        WMessengerOnionLayerProto.__init__(self, WMessengerSimpleCastingLayer.__layer_name__)

    @verify_type(envelope=WMessengerEnvelopeProto, session=WMessengerOnionSessionProto)
    @verify_subclass(from_envelope=WMessengerEnvelopeProto, to_envelope=WMessengerEnvelopeProto)
    def process(self, envelope, session, from_envelope=None, to_envelope=None, **kwargs):
        if isinstance(envelope, from_envelope) is False:
            raise TypeError('Source envelope type mismatch')
        return to_envelope(envelope.message(), meta=envelope)


class WMessengerOnionModeLayerProto(WMessengerOnionLayerProto):
    __doc__ = ' Simple WMessengerOnionLayerProto implementation, that can have different message processing mechanisms\n\t(depends on the "mode" value). This "mode" must be always specified as\n\tmode argument in :meth:`.WMessengerOnionModeLayerProto.process` method. This argument must be the same type\n\t(or be a subclass of the type), that is specified in constructor\n\t'

    @verify_type(name=str, mode_cls=type)
    def __init__(self, name, mode_cls):
        """ Construct new layer

                :param name: layer name
                :param mode_cls: layer's "mode" class
                """
        WMessengerOnionLayerProto.__init__(self, name)
        self._WMessengerOnionModeLayerProto__mode_cls = mode_cls

    @verify_type('paranoid', envelope=WMessengerEnvelopeProto, session=WMessengerOnionSessionProto)
    def process(self, envelope, session, mode=None, **kwargs):
        """ :meth:`.WMessengerOnionLayerProto.process` implementation
                """
        if mode is None:
            raise RuntimeError('"mode" argument must be specified for this object')
        if isinstance(mode, self._WMessengerOnionModeLayerProto__mode_cls) is False:
            raise TypeError('Invalid "mode" argument')
        return self._process(envelope, session, mode, **kwargs)

    @abstractmethod
    @verify_type(envelope=WMessengerEnvelopeProto, session=WMessengerOnionSessionProto)
    def _process(self, envelope, session, mode, **kwargs):
        """ Real processing method.

                :param envelope: original envelope
                :param session:  original session
                :param mode: specified mode
                :param kwargs: layer arguments

                :return: WMessengerEnvelopeProto
                """
        raise NotImplementedError('This method is abstract')


class WMessengerOnionCoderLayerProto(WMessengerOnionModeLayerProto):
    __doc__ = ' Class for layers, that are used for encryption/decryption, encoding/decoding. This layer class works with\n\tstrings and bytes and as a result generates strings and bytes\n\t'

    class Mode(Enum):
        __doc__ = ' Specifies layers mode\n\t\t'
        encode = 1
        decode = 2

    @verify_type(name=str)
    def __init__(self, name):
        """ Construct new layer

                :param name: layer name
                """
        WMessengerOnionModeLayerProto.__init__(self, name, WMessengerOnionCoderLayerProto.Mode)

    @verify_type('paranoid', envelope=WMessengerEnvelopeProto, session=WMessengerOnionSessionProto)
    def _process(self, envelope, session, mode, **kwargs):
        """ :meth:`.WMessengerOnionLayerProto.process` implementation
                """
        if mode == WMessengerOnionCoderLayerProto.Mode.encode:
            return self.encode(envelope, session, **kwargs)
        else:
            return self.decode(envelope, session, **kwargs)

    @abstractmethod
    @verify_type(envelope=(WMessengerTextEnvelope, WMessengerBytesEnvelope), session=WMessengerOnionSessionProto)
    def encode(self, envelope, session, **kwargs):
        """ Encrypt/encode message

                :param envelope: message to encrypt/encode
                :param session: original session
                :return: WMessengerTextEnvelope or WMessengerBytesEnvelope
                """
        raise NotImplementedError('This method is abstract')

    @abstractmethod
    @verify_type(envelope=(WMessengerTextEnvelope, WMessengerBytesEnvelope), session=WMessengerOnionSessionProto)
    def decode(self, envelope, session, **kwargs):
        """ Decrypt/decode message

                :param envelope: message to decrypt/decode
                :param session: original session
                :return: WMessengerTextEnvelope or WMessengerBytesEnvelope
                """
        raise NotImplementedError('This method is abstract')


class WMessengerOnionPackerLayerProto(WMessengerOnionModeLayerProto):
    __doc__ = ' Class for layers, that are used for packing/unpacking, serializing/de-serializing. This layer class\n\tcan pack "any" envelope and produce WMessengerTextEnvelope or WMessengerBytesEnvelope or can\n\tunpack WMessengerTextEnvelope (or WMessengerBytesEnvelope) to "any" object\n\n\t(not "any" but the most)\n\t'

    class Mode(Enum):
        __doc__ = ' Specifies layers mode\n\t\t'
        pack = 1
        unpack = 2

    @verify_type(name=str)
    def __init__(self, name):
        WMessengerOnionModeLayerProto.__init__(self, name, WMessengerOnionPackerLayerProto.Mode)

    @verify_type('paranoid', envelope=WMessengerEnvelopeProto, session=WMessengerOnionSessionProto)
    def _process(self, envelope, session, mode, **kwargs):
        """ :meth:`.WMessengerOnionLayerProto.process` implementation
                """
        if mode == WMessengerOnionPackerLayerProto.Mode.pack:
            return self.pack(envelope, session, **kwargs)
        else:
            return self.unpack(envelope, session, **kwargs)

    @abstractmethod
    @verify_type(envelope=WMessengerEnvelopeProto, session=WMessengerOnionSessionProto)
    def pack(self, envelope, session, **kwargs):
        """ Pack/serialize message

                :param envelope: message to pack/serialize
                :param session: original session
                :return: WMessengerTextEnvelope or WMessengerBytesEnvelope
                """
        raise NotImplementedError('This method is abstract')

    @abstractmethod
    @verify_type(envelope=(WMessengerTextEnvelope, WMessengerBytesEnvelope), session=WMessengerOnionSessionProto)
    def unpack(self, envelope, session, **kwargs):
        """ Unpack/de-serialize message

                :param envelope: message to unpack/de-serialize
                :param session: original session
                :return: WMessengerEnvelopeProto
                """
        raise NotImplementedError('This method is abstract')