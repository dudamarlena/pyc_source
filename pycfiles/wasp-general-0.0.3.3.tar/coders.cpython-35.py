# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/network/messenger/coders.py
# Compiled at: 2017-10-28 14:08:57
# Size of source mod 2**32: 15000 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
from base64 import b64encode, b64decode
from enum import Enum
from wasp_general.verify import verify_type
from wasp_general.crypto.hex import WHex, WUnHex
from wasp_general.crypto.aes import WAES
from wasp_general.crypto.rsa import WRSA
from wasp_general.network.messenger.proto import WMessengerOnionSessionProto
from wasp_general.network.messenger.envelope import WMessengerTextEnvelope, WMessengerBytesEnvelope
from wasp_general.network.messenger.layers import WMessengerOnionCoderLayerProto

class WMessengerFixedModificationLayer(WMessengerOnionCoderLayerProto):
    __doc__ = ' :class:`.WMessengerOnionCoderLayerProto` class implementation. This class applies fixed modification to\n\tspecified messages.\n\n\tIn :meth:`.WMessengerFixedModificationLayer.encode` method this class appends "header" to the message start\n\tor appends "tail" to the message end. One of them must be specified.\n\n\tFor :class:`.WMessengerTextEnvelope` envelope, "header" or "tail" must be "str" type.\n\tFor :class:`.WMessengerBytesEnvelope` envelope, "header" or "tail" must be "bytes" type.\n\t'
    __layer_name__ = 'com.binblob.wasp-general.fixed-modification-layer'

    class Target(Enum):
        __doc__ = ' Modification mode. Specifies whether modification code must be appended to start or to the end\n\t\tof a message\n\t\t'
        head = 1
        tail = 2

    def __init__(self):
        """ Construct new layer
                """
        WMessengerOnionCoderLayerProto.__init__(self, WMessengerFixedModificationLayer.__layer_name__)

    @verify_type(envelope=(WMessengerTextEnvelope, WMessengerBytesEnvelope))
    def __args_check(self, envelope, target, modification_code):
        """ Method checks arguments, that are specified to the
                :meth:`.WMessengerFixedModificationLayer.encode` and :meth:`.WMessengerFixedModificationLayer.decode`
                methods

                :param envelope: same as envelope in :meth:`.WMessengerFixedModificationLayer.encode` and               :meth:`.WMessengerFixedModificationLayer.decode` methods
                :param target: same as target in :meth:`.WMessengerFixedModificationLayer.encode` and           :meth:`.WMessengerFixedModificationLayer.decode` methods
                :param modification_code: same as modification_code in          :meth:`.WMessengerFixedModificationLayer.encode` and :meth:`.WMessengerFixedModificationLayer.decode`           methods

                :return: None
                """
        if target is None:
            raise RuntimeError('"target" argument must be specified for this layer')
        if modification_code is None:
            raise RuntimeError('"modification_code" argument must be specified for this layer')
        if isinstance(target, WMessengerFixedModificationLayer.Target) is False:
            raise TypeError('Invalid "target" argument')
        if isinstance(envelope, WMessengerTextEnvelope) is True:
            if isinstance(modification_code, str) is False:
                raise TypeError('Invalid "modification_code" argument for specified envelope')
        elif isinstance(modification_code, bytes) is False:
            raise TypeError('Invalid "modification_code" argument for specified envelope')

    @verify_type('paranoid', envelope=(WMessengerTextEnvelope, WMessengerBytesEnvelope))
    @verify_type('paranoid', session=WMessengerOnionSessionProto)
    def encode(self, envelope, session, target=None, modification_code=None, **kwargs):
        """ Methods appends 'modification_code' to the specified envelope.

                :param envelope: original envelope
                :param session: original session
                :param target: flag, that specifies whether code must be appended to the start or to the end
                :param modification_code: code to append
                :param kwargs: additional arguments

                :return: WMessengerTextEnvelope or WMessengerBytesEnvelope (depends on the original envelope)
                """
        self._WMessengerFixedModificationLayer__args_check(envelope, target, modification_code)
        if isinstance(envelope, WMessengerTextEnvelope):
            target_envelope_cls = WMessengerTextEnvelope
        else:
            target_envelope_cls = WMessengerBytesEnvelope
        if target == WMessengerFixedModificationLayer.Target.head:
            return target_envelope_cls(modification_code + envelope.message(), meta=envelope)
        else:
            return target_envelope_cls(envelope.message() + modification_code, meta=envelope)

    @verify_type('paranoid', envelope=(WMessengerTextEnvelope, WMessengerBytesEnvelope))
    @verify_type('paranoid', session=WMessengerOnionSessionProto)
    def decode(self, envelope, session, target=None, modification_code=None, **kwargs):
        """ Methods checks envelope for 'modification_code' existence and removes it.

                :param envelope: original envelope
                :param session: original session
                :param target: flag, that specifies whether code must be searched and removed at the start or at the end
                :param modification_code: code to search/remove
                :param kwargs: additional arguments

                :return: WMessengerTextEnvelope or WMessengerBytesEnvelope (depends on the original envelope)
                """
        self._WMessengerFixedModificationLayer__args_check(envelope, target, modification_code)
        message = envelope.message()
        if len(message) < len(modification_code):
            raise ValueError('Invalid message length')
        if isinstance(envelope, WMessengerTextEnvelope):
            target_envelope_cls = WMessengerTextEnvelope
        else:
            target_envelope_cls = WMessengerBytesEnvelope
        if target == WMessengerFixedModificationLayer.Target.head:
            if message[:len(modification_code)] != modification_code:
                raise ValueError('Invalid header in message')
            return target_envelope_cls(message[len(modification_code):], meta=envelope)
        else:
            if message[-len(modification_code):] != modification_code:
                raise ValueError('Invalid tail in message')
            return target_envelope_cls(message[:-len(modification_code)], meta=envelope)


class WMessengerEncodingLayer(WMessengerOnionCoderLayerProto):
    __doc__ = ' This layer can encode str-object to the related encoding (to the bytes-object). Or decode bytes-object from\n\tthe specified encoding (from bytes-object to str-object)\n\t'
    __layer_name__ = 'com.binblob.wasp-general.encoding-layer'

    def __init__(self):
        """ Construct new layer
                """
        WMessengerOnionCoderLayerProto.__init__(self, WMessengerEncodingLayer.__layer_name__)

    @verify_type('paranoid', envelope=WMessengerTextEnvelope, session=WMessengerOnionSessionProto)
    @verify_type(encoding=(str, None))
    def encode(self, envelope, session, encoding=None, **kwargs):
        """ :meth:`.WMessengerOnionCoderLayerProto.encode` method implementation.

                :param envelope: original envelope
                :param session: original session
                :param encoding: encoding to use (default is 'utf-8')
                :param kwargs: additional arguments

                :return: WMessengerBytesEnvelope
                """
        message = envelope.message()
        message = message.encode() if encoding is None else message.encode(encoding)
        return WMessengerBytesEnvelope(message, meta=envelope)

    @verify_type('paranoid', envelope=WMessengerBytesEnvelope, session=WMessengerOnionSessionProto)
    @verify_type(encoding=(str, None))
    def decode(self, envelope, session, encoding=None, **kwargs):
        """ :meth:`.WMessengerOnionCoderLayerProto.decode` method implementation.

                :param envelope: original envelope
                :param session: original session
                :param encoding: encoding to use (default is 'utf-8')
                :param kwargs: additional arguments

                :return: WMessengerTextEnvelope
                """
        message = envelope.message()
        message = message.decode() if encoding is None else message.decode(encoding)
        return WMessengerTextEnvelope(message, meta=envelope)


class WMessengerHexLayer(WMessengerOnionCoderLayerProto):
    __doc__ = ' :class:`.WMessengerOnionCoderLayerProto` class implementation. This class translate message to corresponding\n\thex-string, or decodes it from hex-string to original binary representation.\n\t'
    __layer_name__ = 'com.binblob.wasp-general.hex-layer'

    def __init__(self):
        """ Construct new layer
                """
        WMessengerOnionCoderLayerProto.__init__(self, WMessengerHexLayer.__layer_name__)

    @verify_type('paranoid', session=WMessengerOnionSessionProto)
    @verify_type(envelope=WMessengerBytesEnvelope)
    def encode(self, envelope, session, **kwargs):
        """ :meth:`.WMessengerOnionCoderLayerProto.encode` method implementation.

                :param envelope: original envelope
                :param session: original session
                :param kwargs: additional arguments

                :return: WMessengerTextEnvelope
                """
        return WMessengerTextEnvelope(str(WHex(envelope.message())), meta=envelope)

    @verify_type('paranoid', session=WMessengerOnionSessionProto)
    @verify_type(envelope=WMessengerTextEnvelope)
    def decode(self, envelope, session, **kwargs):
        """ :meth:`.WMessengerOnionCoderLayerProto.decode` method implementation.

                :param envelope: original envelope
                :param session: original session
                :param kwargs: additional arguments

                :return: WMessengerBytesEnvelope
                """
        return WMessengerBytesEnvelope(bytes(WUnHex(envelope.message())), meta=envelope)


class WMessengerBase64Layer(WMessengerOnionCoderLayerProto):
    __doc__ = ' :class:`.WMessengerOnionCoderLayerProto` class implementation. This class translate binary message\n\tto the corresponding base64 encoded bytes, or decodes it from base64 encoded bytes to the original binary\n\trepresentation.\n\t'
    __layer_name__ = 'com.binblob.wasp-general.base64-layer'

    def __init__(self):
        """ Construct new layer
                """
        WMessengerOnionCoderLayerProto.__init__(self, WMessengerBase64Layer.__layer_name__)

    @verify_type('paranoid', session=WMessengerOnionSessionProto)
    @verify_type(envelope=WMessengerBytesEnvelope)
    def encode(self, envelope, session, **kwargs):
        """ :meth:`.WMessengerOnionCoderLayerProto.encode` method implementation.

                :param envelope: original envelope
                :param session: original session
                :param kwargs: additional arguments

                :return: WMessengerBytesEnvelope
                """
        return WMessengerBytesEnvelope(b64encode(envelope.message()), meta=envelope)

    @verify_type('paranoid', session=WMessengerOnionSessionProto)
    @verify_type(envelope=WMessengerBytesEnvelope)
    def decode(self, envelope, session, **kwargs):
        """ :meth:`.WMessengerOnionCoderLayerProto.decode` method implementation.

                :param envelope: original envelope
                :param session: original session
                :param kwargs: additional arguments

                :return: WMessengerBytesEnvelope
                """
        return WMessengerBytesEnvelope(b64decode(envelope.message()), meta=envelope)


class WMessengerAESLayer(WMessengerOnionCoderLayerProto):
    __doc__ = ' :class:`.WMessengerOnionCoderLayerProto` class implementation. This class encrypts/decrypts message with\n\tthe specified AES cipher\n\t'
    __layer_name__ = 'com.binblob.wasp-general.aes-layer'

    def __init__(self):
        """ Construct new layer
                """
        WMessengerOnionCoderLayerProto.__init__(self, WMessengerAESLayer.__layer_name__)

    @verify_type('paranoid', session=WMessengerOnionSessionProto)
    @verify_type(envelope=WMessengerBytesEnvelope)
    @verify_type(aes_cipher=WAES)
    def encode(self, envelope, session, aes_cipher=None, **kwargs):
        """ :meth:`.WMessengerOnionCoderLayerProto.encode` method implementation.

                :param envelope: original envelope
                :param session: original session
                :param aes_cipher: cipher to use
                :param kwargs: additional arguments

                :return: WMessengerBytesEnvelope
                """
        return WMessengerBytesEnvelope(aes_cipher.encrypt(envelope.message()), meta=envelope)

    @verify_type('paranoid', session=WMessengerOnionSessionProto)
    @verify_type(envelope=WMessengerBytesEnvelope)
    @verify_type(aes_cipher=WAES)
    def decode(self, envelope, session, aes_cipher=None, **kwargs):
        """ :meth:`.WMessengerOnionCoderLayerProto.decode` method implementation.

                :param envelope: original envelope
                :param session: original session
                :param aes_cipher: cipher to use
                :param kwargs: additional arguments

                :return: WMessengerBytesEnvelope
                """
        return WMessengerBytesEnvelope(aes_cipher.decrypt(envelope.message(), decode=False), meta=envelope)


class WMessengerRSALayer(WMessengerOnionCoderLayerProto):
    __doc__ = ' :class:`.WMessengerOnionCoderLayerProto` class implementation. This class encrypts/decrypts message with\n\tspecified RSA cipher\n\t'
    __layer_name__ = 'com.binblob.wasp-general.rsa-layer'

    def __init__(self):
        """ Construct new layer
                """
        WMessengerOnionCoderLayerProto.__init__(self, WMessengerRSALayer.__layer_name__)

    @verify_type('paranoid', session=WMessengerOnionSessionProto, public_key=WRSA.wrapped_class, sha_digest_size=int)
    @verify_type(envelope=WMessengerBytesEnvelope)
    def encode(self, envelope, session, public_key=None, sha_digest_size=32, **kwargs):
        """ :meth:`.WMessengerOnionCoderLayerProto.encode` method implementation.

                :param envelope: original envelope
                :param session: original session
                :param public_key: public key to encrypt
                :param sha_digest_size: SHA digest size to use
                :param kwargs: additional arguments

                :return: WMessengerBytesEnvelope
                """
        message = WRSA.encrypt(envelope.message(), public_key, sha_digest_size=sha_digest_size)
        return WMessengerBytesEnvelope(message, meta=envelope)

    @verify_type('paranoid', session=WMessengerOnionSessionProto, private_key=WRSA.wrapped_class)
    @verify_type('paranoid', sha_digest_size=int)
    @verify_type(envelope=WMessengerBytesEnvelope)
    def decode(self, envelope, session, private_key=None, sha_digest_size=32, **kwargs):
        """ :meth:`.WMessengerOnionCoderLayerProto.decode` method implementation.

                :param envelope: original envelope
                :param session: original session
                :param private_key: private key to decrypt
                :param sha_digest_size: SHA digest size to use
                :param kwargs: additional arguments

                :return: WMessengerBytesEnvelope
                """
        message = WRSA.decrypt(envelope.message(), private_key, sha_digest_size=sha_digest_size)
        return WMessengerBytesEnvelope(message, meta=envelope)