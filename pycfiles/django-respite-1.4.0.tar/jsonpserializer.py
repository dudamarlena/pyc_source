# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jgorset/code/python/libraries/respite/respite/serializers/jsonpserializer.py
# Compiled at: 2012-09-28 03:36:32
try:
    import json
except ImportError:
    from django.utils import simplejson as json

from respite.serializers.jsonserializer import JSONSerializer

class JSONPSerializer(JSONSerializer):

    def serialize(self, request):
        data = super(JSONPSerializer, self).serialize(request)
        if 'callback' in request.GET:
            callback = request.GET['callback']
        else:
            callback = 'callback'
        return '%s(%s)' % (callback, data)