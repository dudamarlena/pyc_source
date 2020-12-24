# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/pycast/common/json_encoder.py
# Compiled at: 2015-05-28 05:27:59
import json
from pycastobject import PyCastObject

class PycastEncoder(json.JSONEncoder, PyCastObject):
    """Encodes a PyCastObject to json."""

    def default(self, obj):
        return obj.to_twodim_list()