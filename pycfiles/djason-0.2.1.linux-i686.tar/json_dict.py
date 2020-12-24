# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dusty/code/egetime/venv/lib/python2.7/site-packages/djason/json_dict.py
# Compiled at: 2011-05-12 14:33:59
"""
Serialize data to/from JSON storing the results in an object with
possible extra attributes.

So where the djason.json serializer would return
[{attr1: val1},...] this one will return
{akey: avalue, anotherkey:anothervalue, objects:[{attr1:val1},...]}
"""
from django.utils import simplejson
from json import Serializer as JsonSerializer
from django.core.serializers.json import Deserializer as JSONDeserializer, DjangoJSONEncoder

class Serializer(JsonSerializer):
    """
    Convert a queryset to JSON.
    """

    def end_serialization(self):
        """Output a JSON encoded queryset."""
        self.options.pop('stream', None)
        self.options.pop('fields', None)
        self.options.pop('excludes', None)
        self.options.pop('relations', None)
        self.options.pop('extras', None)
        self.options.pop('use_natural_keys', None)
        self.use_httpresponse = self.options.pop('httpresponse', None)
        attributes = self.options.pop('attributes', {})
        list_name = self.options.pop('list_name', 'objects')
        attributes[list_name] = self.objects
        simplejson.dump(attributes, self.stream, cls=DjangoJSONEncoder, **self.options)
        return


Deserializer = JSONDeserializer