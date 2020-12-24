# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dusty/code/egetime/venv/lib/python2.7/site-packages/djason/httpjson.py
# Compiled at: 2011-05-12 14:16:24
"""
Serialize data to/from JSON
"""
from django.utils import simplejson
from json import Serializer as JsonSerializer
from django.core.serializers.json import Deserializer as JSONDeserializer, DjangoJSONEncoder
from django.http import HttpResponse

class Serializer(JsonSerializer):
    """
    Wrap a json serializer in an HttpResponse
    """

    def getvalue(self):
        return HttpResponse(super(Serializer, self).getvalue())


Deserializer = JSONDeserializer