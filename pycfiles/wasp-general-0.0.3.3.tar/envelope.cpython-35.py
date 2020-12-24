# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/network/messenger/envelope.py
# Compiled at: 2017-10-28 14:20:54
# Size of source mod 2**32: 3247 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
from wasp_general.verify import verify_type
from wasp_general.network.messenger.proto import WMessengerEnvelopeProto

class WMessengerEnvelope(WMessengerEnvelopeProto):
    __doc__ = ' Simple :class:`.WMessengerEnvelopeProto` implementation. "Meta-dictionary" is used as is without any\n\trestrictions or limitations, so any further envelopes (envelopes that uses this envelope as meta) can rewrite\n\tor remove saved information\n\t'

    @verify_type(meta=(WMessengerEnvelopeProto, dict, None))
    def __init__(self, data, meta=None):
        """ Construct new envelope

                :param data: original message
                :param meta: envelope meta-data to copy
                """
        self._WMessengerEnvelope__data = data
        self._WMessengerEnvelope__meta = {}
        if meta is not None:
            if isinstance(meta, WMessengerEnvelopeProto) is True:
                if isinstance(meta, WMessengerEnvelope) is False:
                    raise TypeError('meta must be WMessengerEnvelope (or derived classes) object')
                self._WMessengerEnvelope__meta = meta.meta()
        elif isinstance(meta, dict):
            self._WMessengerEnvelope__meta = meta.copy()

    def message(self):
        """ Return original message

                :return: any type
                """
        return self._WMessengerEnvelope__data

    def meta(self):
        """ Return envelope dictionary copy

                :return: dict
                """
        return self._WMessengerEnvelope__meta.copy()

    @verify_type(key=str)
    def add_meta(self, key, value):
        """ Add meta-information (value) for the given key

                :param key: meta-key
                :param value: meta-value
                :return: None
                """
        self._WMessengerEnvelope__meta[key] = value


class WMessengerTextEnvelope(WMessengerEnvelope):
    __doc__ = ' Envelope for str-objects\n\t'

    @verify_type(data=str, meta=(WMessengerEnvelopeProto, dict, None))
    def __init__(self, data, meta=None):
        WMessengerEnvelope.__init__(self, data, meta=meta)


class WMessengerBytesEnvelope(WMessengerEnvelope):
    __doc__ = ' Envelope for bytes-objects\n\t'

    @verify_type(data=bytes, meta=(WMessengerEnvelopeProto, dict, None))
    def __init__(self, data, meta=None):
        WMessengerEnvelope.__init__(self, data, meta=meta)


class WMessengerDictEnvelope(WMessengerEnvelope):
    __doc__ = ' Envelope for dict-objects (dictionary objects)\n\t'

    @verify_type(data=dict, meta=(WMessengerEnvelopeProto, dict, None))
    def __init__(self, data, meta=None):
        WMessengerEnvelope.__init__(self, data, meta=meta)