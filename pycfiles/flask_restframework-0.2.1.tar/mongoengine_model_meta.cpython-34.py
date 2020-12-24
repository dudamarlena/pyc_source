# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stas/workspace/partners/flask_restframework/flask_restframework/utils/mongoengine_model_meta.py
# Compiled at: 2017-06-28 10:44:39
# Size of source mod 2**32: 1011 bytes
import six
from mongoengine import fields as db
from flask_restframework import fields
FIELD_MAPPING = {db.ObjectIdField: fields.StringField, 
 db.StringField: fields.StringField, 
 db.BooleanField: fields.BooleanField, 
 db.DateTimeField: fields.DateTimeField, 
 db.EmbeddedDocumentField: fields.EmbeddedField, 
 db.ReferenceField: fields.PrimaryKeyRelatedField, 
 db.IntField: fields.IntegerField, 
 db.SequenceField: fields.SequenceField, 
 db.URLField: fields.URLField, 
 db.EmbeddedDocumentListField: fields.ListField, 
 db.ListField: fields.ListField, 
 db.DictField: fields.DictField, 
 db.DecimalField: fields.DecimalField}

def get_fields(model):
    """Returns dict <fieldName>: <fieldClass>"""
    out = {}
    for key, value in six.iteritems(model._fields):
        out[key] = value.__class__

    return out


def initialize_field(field):
    pass


def get_field(model, key):
    """for model returns its field instance with name key"""
    return model._fields[key]