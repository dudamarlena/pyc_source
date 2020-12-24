# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.7/site-packages/pycast/common/json_encoder.py
# Compiled at: 2015-05-28 05:27:59
import json
from pycastobject import PyCastObject

class PycastEncoder(json.JSONEncoder, PyCastObject):
    """Encodes a PyCastObject to json."""

    def default(self, obj):
        return obj.to_twodim_list()