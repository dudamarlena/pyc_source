# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/sqs/jsonmessage.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 1755 bytes
import base64
from boto.sqs.message import MHMessage
from boto.exception import SQSDecodeError
from boto.compat import json

class JSONMessage(MHMessage):
    __doc__ = "\n    Acts like a dictionary but encodes it's data as a Base64 encoded JSON payload.\n    "

    def decode(self, value):
        try:
            value = base64.b64decode(value.encode('utf-8')).decode('utf-8')
            value = json.loads(value)
        except:
            raise SQSDecodeError('Unable to decode message', self)

        return value

    def encode(self, value):
        value = json.dumps(value)
        return base64.b64encode(value.encode('utf-8')).decode('utf-8')