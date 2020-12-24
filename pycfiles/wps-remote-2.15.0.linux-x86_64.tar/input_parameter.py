# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alessio/Envs/remote-wps/lib/python2.7/site-packages/wpsremote/input_parameter.py
# Compiled at: 2018-09-14 04:52:53
__author__ = 'Alessio Fabiani'
__copyright__ = 'Copyright 2016 Open Source Geospatial Foundation - all rights reserved'
__license__ = 'GPL'
import string, datetime, json

class InputParameter(object):

    def __init__(self, name):
        self._name = name
        self._alias = None
        self._type = None
        self._title = None
        self._description = None
        self._min = 0
        self._max = 1
        self._default = None
        self._formatter = None
        self._input_mime_type = None
        self._allowed_chars = string.printable.replace('-', '').replace(' ', '')
        self._value = None
        return

    def inject_values(self, paremeters_types_defs):
        for k, v in paremeters_types_defs.items():
            if hasattr(self, '_' + k):
                setattr(self, '_' + k, v)

        self._min = int(self._min)
        self._max = int(self._max)

    def set_actual_value(self, value):
        if type(value) is not list:
            self._value = [
             value]
        else:
            self._value = value

    def has_value(self):
        return self._value != None

    def get_value(self):
        return self._value

    def _type_checking(self, value):
        try:
            if self._type == 'int':
                int(value)
                return self._type
            else:
                if self._type == 'float':
                    float(value)
                    return self._type
                if self._type == 'string':
                    return all(c in self._allowed_chars for c in value)
                if self._type == 'datetime' and self._formatter != None:
                    datetime.datetime.strptime(value, self._formatter)
                    return self._type
                if self._type == 'application/json':
                    json.loads(value)
                    return self._type
                return False

        except:
            return False

        return

    def validate(self):
        if not self.has_value():
            raise Exception('cannot find a value for parameter ' + self.get_name())
        if not (self._min <= len(self._value) and len(self._value) <= self._max):
            raise Exception('Actual value for parameter has wrong multiplicity')
        res = map(self._type_checking, self._value)
        res = list(set(res))
        if len(res) == 1 and res[0]:
            return True
        raise Exception('Bad type')

    def get_name(self):
        if self._alias != None:
            return self._alias
        else:
            return self._name

    def get_input_mime_type(self):
        return self._input_mime_type

    def get_name_no_alias(self):
        return self._name

    def get_cmd_line(self):
        pass

    def as_json_string(self):
        res = {}
        attrib_to_convert = [
         '_type', '_title', '_description', '_min', '_max', '_default', '_input_mime_type']
        attribute_list = [ a for a in dir(self) if not a.startswith('__') and not callable(getattr(self, a)) ]
        attribute_list_filtered = [ x for x in attribute_list if x in attrib_to_convert ]
        for a in attribute_list_filtered:
            res[a[1:]] = getattr(self, a)

        return json.dumps(res)