# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/serializer.py
# Compiled at: 2018-12-17 11:51:20
from __future__ import absolute_import
__all__ = [
 'start']
import json, binascii
from autobahn import wamp
from autobahn.wamp.test.test_serializer import generate_test_messages

def start(outfilename, debug=False):
    with open(outfilename, 'wb') as (outfile):
        ser_json = wamp.serializer.JsonSerializer()
        ser_msgpack = wamp.serializer.MsgPackSerializer()
        res = []
        for msg in generate_test_messages():
            case = {}
            case['name'] = str(msg)
            case['rmsg'] = msg.marshal()
            bytes, binary = ser_json.serialize(msg)
            case['json'] = bytes
            bytes, binary = ser_msgpack.serialize(msg)
            case['msgpack'] = binascii.hexlify(bytes)
            res.append(case)

        outfile.write(json.dumps(res, indent=3))