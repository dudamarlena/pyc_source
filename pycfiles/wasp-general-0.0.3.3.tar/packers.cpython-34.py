# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ale/progr/github/wasp-general/wasp_general/network/messenger/packers.py
# Compiled at: 2017-06-28 15:28:31
# Size of source mod 2**32: 2701 bytes
from wasp_general.version import __author__, __version__, __credits__, __license__, __copyright__, __email__
from wasp_general.version import __status__
import json
from datetime import datetime
from wasp_general.verify import verify_type
from wasp_general.datetime import utc_datetime
from wasp_general.network.messenger.proto import WMessengerEnvelopeProto, WMessengerOnionSessionProto
from wasp_general.network.messenger.layers import WMessengerOnionPackerLayerProto
from wasp_general.network.messenger.envelope import WMessengerEnvelope, WMessengerTextEnvelope

class WMessengerJSONPacker(WMessengerOnionPackerLayerProto):
    __layer_name__ = 'com.binblob.wasp-general.json-packer-layer'

    class JSONEncoder(json.encoder.JSONEncoder):

        def default(self, o):
            if isinstance(o, set) is True:
                return list(o)
            if isinstance(o, bytes):
                return [x for x in o]
            if isinstance(o, datetime):
                return utc_datetime(o, local_value=False).isoformat()
            return json.encoder.JSONEncoder.default(self, o)

    def __init__(self):
        """ Construct new layer
                """
        WMessengerOnionPackerLayerProto.__init__(self, WMessengerJSONPacker.__layer_name__)

    @verify_type('paranoid', session=WMessengerOnionSessionProto)
    @verify_type(envelope=WMessengerEnvelopeProto)
    def pack(self, envelope, session, **kwargs):
        json_data = json.dumps(envelope.message(), cls=WMessengerJSONPacker.JSONEncoder)
        return WMessengerTextEnvelope(json_data, meta=envelope)

    @verify_type('paranoid', session=WMessengerOnionSessionProto)
    @verify_type(envelope=WMessengerTextEnvelope)
    def unpack(self, envelope, session, **kwargs):
        return WMessengerEnvelope(json.loads(envelope.message()), meta=envelope)