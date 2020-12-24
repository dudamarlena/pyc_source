# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/app/tcrudge/response.py
# Compiled at: 2016-12-08 09:48:39
# Size of source mod 2**32: 1021 bytes
"""
Functions to handle different response formats must receive two arguments:
    * handler: subclass of tornado.web.RequestHandler;
    * answer: dictionary with response data.

And it should return bytes.
"""
import json, msgpack
from tcrudge.utils.json import json_serial

def response_json(handler, response):
    """
    Default JSON response.

    Sets JSON content type to given handler.

    Serializes result with JSON serializer and sends JSON as response body.

    :return: Bytes of JSONised response
    :rtype: bytes
    """
    handler.set_header('Content-Type', 'application/json')
    return json.dumps(response, default=json_serial)


def response_msgpack(handler, response):
    """
    Optional MSGPACK response.

    Sets MSGPACK content type to given handler.

    Packs response with MSGPACK.

    :return: Bytes of MSGPACK packed response
    :rtype: bytes
    """
    handler.set_header('Content-Type', 'application/x-msgpack')
    return msgpack.packb(response, default=json_serial)