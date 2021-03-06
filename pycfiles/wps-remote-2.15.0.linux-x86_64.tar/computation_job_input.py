# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alessio/Envs/remote-wps/lib/python2.7/site-packages/wpsremote/computation_job_input.py
# Compiled at: 2018-09-14 05:10:56
__author__ = 'Alessio Fabiani'
__copyright__ = 'Copyright 2016 Open Source Geospatial Foundation - all rights reserved'
__license__ = 'GPL'
import string, datetime, json

class ComputationJobInput(object):

    def __init__(self, name, input_type, title, description, default=None, formatter=None, input_mime_type=None):
        self._name = name
        self._type = input_type
        self._default = default
        self._formatter = formatter
        self._title = title
        self._description = description
        self._input_mime_type = input_mime_type
        self._value = None
        self._value_converted = None
        self._allowed_chars = string.printable.replace(' ', '')
        self._allowed_chars_url = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~:/?#[]@!$&'()*+,;="
        return

    def _validate_and_convert(self, value):
        if self._type == 'int':
            return int(value)
        if self._type == 'float':
            return float(value)
        if self._type == 'string':
            if all(c in self._allowed_chars for c in value):
                return value
        else:
            if self._type == 'url':
                if all(c in self._allowed_chars_url for c in value):
                    return value
            elif self._type in ('application/json', 'application/xml'):
                return json.loads(value)
            if self._type == 'datetime':
                if self._formatter:
                    try:
                        date_value = value.strftime(self._formatter)
                        return date_value
                    except:
                        pass

                if all(c in self._allowed_chars for c in value):
                    return value
        raise TypeError('Cannot validate and convert value ' + str(value) + ' for type ' + self._type)

    def _type_checking(self, value):
        try:
            self._validate_and_convert(value)
            return self._type
        except TypeError:
            return False

    def validate(self):
        if not self.has_value():
            raise TypeError('cannot find a value for parameter ' + self.get_name())
        res = map(self._type_checking, self._value)
        res = list(set(res))
        if len(res) == 1 and res[0]:
            self._value_converted = map(self._validate_and_convert, self._value)
            return True
        raise TypeError('cannot validate value ' + str(self._value) + ' for parameter ' + self.get_name() + ' with type ' + self._type)

    def set_value(self, value):
        if type(value) is not list:
            self._value = [
             value]
        else:
            self._value = value
        res = False
        try:
            res = self.validate()
            if not res:
                raise TypeError('cannot set value ' + str(self._value) + ' for parameter ' + self.get_name() + ' with type ' + self._type)
        except:
            raise TypeError('cannot set value ' + str(self._value) + ' for parameter ' + self.get_name() + ' with type ' + self._type)

    def get_value(self):
        if type(self._value_converted) is list and len(self._value_converted) == 1:
            return self._value_converted[0]
        else:
            return self._value_converted

    def get_type(self):
        return self._type

    def get_input_mime_type(self):
        return self._input_mime_type

    def get_value_string(self):
        if type(self._value) is list and len(self._value) == 1:
            if type(self._value[0]) is datetime.datetime:
                return self._value[0].strftime(self._formatter)
            else:
                return self._value[0]

        else:
            return self._value

    def get_value_as_JSON_literal(self):
        res = map(self._JSON_token_converter, self._value_converted)
        if type(res) is list and len(res) == 1:
            return res[0]
        else:
            return res

    def _JSON_token_converter(self, value):
        if self._type == 'int' or self._type == 'float':
            return str(value)
        if self._type == 'string':
            return "'" + str(value) + "'"
        if self._type == 'datetime':
            return "'" + value.strftime(self._formatter) + "'"
        if self._type == 'application/json':
            raise TypeError('cannot convert json in json')
        else:
            raise TypeError('unknown type for value ' + self.get_name())

    def has_value(self):
        return self._value != None

    def get_name(self):
        return self._name

    def as_json_string(self):
        res = {}
        attrib_to_convert = [
         '_type', '_title', '_default', '_description', '_min', '_max', '_input_mime_type']
        attribute_list = [ a for a in dir(self) if not a.startswith('__') and not callable(getattr(self, a)) ]
        attribute_list_filtered = [ x for x in attribute_list if x in attrib_to_convert ]
        for a in attribute_list_filtered:
            res[a[1:]] = getattr(self, a)

        return json.dumps(res)