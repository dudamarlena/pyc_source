# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/easyapi/encoder.py
# Compiled at: 2014-10-23 17:55:30
from enum import Enum
from rest_framework.renderers import JSONRenderer
from rest_framework.utils.encoders import JSONEncoder
from django.db import models
from easyapi.fields import enum_value
from easyapi.serializer import serialize_instance
__author__ = 'mikhailturilin'

class ModelJSONEncoder(JSONEncoder):

    def default(self, o):
        if isinstance(o, models.Model):
            return serialize_instance(o)
        else:
            if isinstance(o, Enum):
                return enum_value(o)
            if hasattr(o, 'to_json'):
                return o.to_json()
            return super(ModelJSONEncoder, self).default(o)


class ModelJSONRenderer(JSONRenderer):
    encoder_class = ModelJSONEncoder