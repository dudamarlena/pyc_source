# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mauricio.abreua/Code/django-rest-framework-orjson/rest_framework_orjson/renderers.py
# Compiled at: 2019-07-19 07:57:42
# Size of source mod 2**32: 703 bytes
import orjson
from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList

class ORJSONRenderer(JSONRenderer):

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render `data` into JSON, returning a bytestring.
        """
        if data is None:
            return bytes()
        return orjson.dumps(data, default=serialize_arbitrary_type)


def serialize_arbitrary_type(data):
    if isinstance(data, ReturnDict):
        return dict(data)
    if isinstance(data, ReturnList):
        items = []
        for item in data:
            items.append(dict(item))

        return list(items)