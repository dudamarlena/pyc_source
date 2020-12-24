# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../flask_peewee/serializer.py
# Compiled at: 2018-01-17 11:50:43
import datetime, sys, uuid
from peewee import Model
from flask_peewee.utils import get_dictionary_from_model
from flask_peewee.utils import get_model_from_dictionary

class Serializer(object):
    date_format = '%Y-%m-%d'
    time_format = '%H:%M:%S'
    datetime_format = (' ').join([date_format, time_format])

    def convert_value(self, value):
        if isinstance(value, datetime.datetime):
            return value.strftime(self.datetime_format)
        else:
            if isinstance(value, datetime.date):
                return value.strftime(self.date_format)
            if isinstance(value, datetime.time):
                return value.strftime(self.time_format)
            if isinstance(value, Model):
                return value._pk
            if isinstance(value, uuid.UUID):
                return str(value)
            return value

    def clean_data(self, data):
        for key, value in data.items():
            if isinstance(value, dict):
                self.clean_data(value)
            elif isinstance(value, (list, tuple)):
                data[key] = map(self.clean_data, value)
            else:
                data[key] = self.convert_value(value)

        return data

    def serialize_object(self, obj, fields=None, exclude=None):
        data = get_dictionary_from_model(obj, fields, exclude)
        return self.clean_data(data)


class Deserializer(object):

    def deserialize_object(self, model, data):
        return get_model_from_dictionary(model, data)