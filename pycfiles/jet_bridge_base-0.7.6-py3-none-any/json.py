# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/responses/json.py
# Compiled at: 2019-10-06 13:09:22
import json
from jet_bridge_base import encoders
from jet_bridge_base.responses.base import Response

class JSONResponse(Response):
    headers = {'Content-Type': 'application/json'}
    encoder_class = encoders.JSONEncoder

    def render(self):
        if self.data is None:
            return bytes()
        else:
            return json.dumps(self.data, cls=self.encoder_class)