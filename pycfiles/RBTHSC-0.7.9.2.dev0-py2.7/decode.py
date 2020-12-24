# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\rbtools\api\decode.py
# Compiled at: 2017-04-19 05:14:02
from __future__ import unicode_literals
import json
from rbtools.api.utils import parse_mimetype
DECODER_MAP = {}

def DefaultDecoder(payload):
    """Default decoder for API payloads.

    The default decoder is used when a decoder is not found in the
    DECODER_MAP. This will stick the body of the response into the
    'data' field.
    """
    return {b'resource': {b'data': payload}}


DEFAULT_DECODER = DefaultDecoder

def JsonDecoder(payload):
    return json.loads(payload)


DECODER_MAP[b'application/json'] = JsonDecoder

def decode_response(payload, mime_type):
    """Decode a Web API response.

    The body of a Web API response will be decoded into a dictionary,
    according to the provided mime_type.
    """
    mime = parse_mimetype(mime_type)
    format = b'%s/%s' % (mime[b'main_type'], mime[b'format'])
    if format in DECODER_MAP:
        decoder = DECODER_MAP[format]
    else:
        decoder = DEFAULT_DECODER
    return decoder(payload)