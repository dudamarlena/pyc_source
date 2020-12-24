# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jgorset/code/python/libraries/respite/respite/serializers/jsonserializer.py
# Compiled at: 2012-09-28 03:36:32
try:
    import json
except ImportError:
    from django.utils import simplejson as json

from respite.serializers.base import Serializer

class JSONSerializer(Serializer):

    def serialize(self, request):
        data = super(JSONSerializer, self).serialize(request)
        return json.dumps(data, ensure_ascii=False)