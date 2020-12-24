# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dusty/code/egetime/venv/lib/python2.7/site-packages/djson/json.py
# Compiled at: 2010-11-28 12:12:42
"""
Serialize data to/from JSON
"""
from django.utils import simplejson
from python import Serializer as PythonSerializer
from django.core.serializers.json import Deserializer as JSONDeserializer, DjangoJSONEncoder

class Serializer(PythonSerializer):
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
        simplejson.dump(self.objects, self.stream, cls=DjangoJSONEncoder, **self.options)
        return

    def getvalue(self):
        """
        Return the fully serialized queryset (or None if the output stream
        is not seekable).
        """
        if callable(getattr(self.stream, 'getvalue', None)):
            return self.stream.getvalue()
        else:
            return


Deserializer = JSONDeserializer