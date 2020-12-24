# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/opencontainers/struct.py
# Compiled at: 2019-11-06 10:15:39
# Size of source mod 2**32: 13013 bytes
from opencontainers.logger import bot
from datetime import datetime
import copy, json, re

class StructAttr(object):
    __doc__ = "A struct attribute holds a name, jsonName, value, attribute type,\n       and if it's required or not. The name should hold the parameter name\n       as reflected in the original (usually GoLang) implementation, while\n       the jsonName is how it should be serialized to json.\n\n       Parameters\n       ==========\n       name: the name (key) for the attribute\n       attType: the attribute type (a python type), can be provided in list\n       required: boolean if required or not\n       jsonName: the name to serialize to json (not required, will use name)\n       value: optionally, provide a value on init\n       omitempty: if true, don't serialize with response.       \n    "

    def __init__(self, name, attType, required, jsonName=None, value=None, omitempty=True, regexp=None, hide=False):
        self.name = name
        self.value = value
        self.attType = attType
        self.required = required
        self.regexp = regexp or ''
        self.jsonName = jsonName or name
        self.omitempty = omitempty
        self.hide = hide

    def __str__(self):
        return '<opencontainers.struct.StructAttr-%s:%s>' % (self.name, self.value)

    def __repr__(self):
        return self.__str__()

    def _is_struct(self, attType=None):
        """determine if an attType is another struct we need to populate
        """
        if not attType:
            attType = self.attType
        try:
            return Struct in attType.__bases__ or StrStruct in attType.__bases__ or IntStruct in attType.__bases__
        except:
            return False

    def set(self, value):
        """set a new value, and validate the type. Return true if set
        """
        if self._is_struct():
            newStruct = self.attType()
            value = newStruct.load(value)
        else:
            if isinstance(self.attType, list):
                if self.attType:
                    child = self.attType[0]
                    if self._is_struct(child):
                        if isinstance(value, list):
                            values = []
                            for v in value:
                                newStruct = child()
                                values.append(newStruct.load(v))

                            value = values
                        else:
                            newStruct = child()
                            value = newStruct.load(value)
            else:
                return self.validate_regexp(value) or False
            if self.validate_type(value):
                self.value = value
                return True
            return False

    def to_dict(self):
        """return a dictionary representation of the attribute. This won't
           be called unless the attribute in question is a struct.
        """
        if isinstance(self.value, (str, int)):
            return self.value
        if isinstance(self.value, list):
            items = []
            for item in self.value:
                if isinstance(item, (str, int)):
                    items.append(item)
                elif isinstance(item, (Struct, StrStruct, IntStruct)):
                    items.append(item.to_dict())
                else:
                    items.append(item)

            return items
        return self.value.to_dict()

    def validate_datetime(self, value):
        """validate a datetime string, but be generous to only check day,
           month, year. This is a road nobody wants to go down.
        """
        value = value.split('T')[0]
        try:
            datetime.strptime(value, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def validate_regexp(self, value):
        """validate a string or nested string values against a regular
           expression. Return True if valid or not applicable, False otherwise
        """
        if not self.regexp:
            return True
        if not isinstance(value, list):
            value = [
             value]
        for entry in value:
            if isinstance(entry, str):
                re.search(self.regexp, entry) or bot.error('%s failed regex validation %s ' % (entry, self.regexp))
                return False

        return True

    def validate_type(self, value):
        """ensure that an attribute is of the correct type. If we are given
           a list as type, then the value within it is the type we are checking.
        """
        if isinstance(self.attType, list):
            if not isinstance(value, list):
                return False
            if self.attType:
                attType = self.attType[0]
                for entry in value:
                    if not isinstance(entry, attType):
                        return False

        else:
            if self.attType == datetime:
                return self.validate_datetime(value)
            return isinstance(value, self.attType) or False
        return True


class Struct(object):
    __doc__ = 'a Struct is a general base class that allows for printing \n       and validating a set of attributes according to their defined subclass.\n       the subclass should have an init function that uses the functions\n       here to add required attributes.\n    '

    def __init__(self):
        self.attrs = {}

    def newAttr(self, name, attType, required=False, jsonName=None, omitempty=True, regexp='', hide=False):
        """add a new attribute, including a name, json key to dump,
           type, and if required. We don't need a value here. You can
           also update a current attribute here.

           Parameters
           ==========
           name: the name (key) for the attribute
           attType: the attribute type (a python type), can be provided in list
           required: boolean if required or not
           jsonName: the name to serialize to json (not required, will use name)
           omitempty: if true, don't serialize with response.
           regexp: if a string is provided as the type (or nested), check against
        """
        self.attrs[name] = StructAttr(name=name, attType=attType,
          required=required,
          jsonName=jsonName,
          omitempty=omitempty,
          regexp=regexp,
          hide=hide)

    def _clear_values(self):
        """if a load is done, we remove previously loaded values for any
           attributes
        """
        for name, att in self.attrs.items():
            self.attrs[name].value = None

    def to_dict(self):
        """return a Struct as a dictionary, must be valid
        """
        lookup = {str: '', int: None, list: [], dict: {}}
        if self.validate():
            result = {}
            for name, att in self.attrs.items():
                if not att.value:
                    if att.omitempty or att.hide:
                        continue
                    if not att.value:
                        value = lookup.get(att.attType, [])
                        result[att.jsonName] = value
                    elif att._is_struct() or isinstance(att.value, list):
                        result[att.jsonName] = att.to_dict()
                    else:
                        result[att.jsonName] = att.value

            return result

    def to_json(self):
        """get the dictionary of a struct and return pretty printed json
        """
        result = self.to_dict()
        if result:
            result = json.dumps(result, indent=4)
        return result

    def add(self, name, value):
        """add a value to an existing attribute, normally when used by a client
        """
        if name not in self.attrs:
            bot.exit('%s is not a valid attribute.' % name)
        attr = self.attrs[name]
        if value:
            if not attr.set(value):
                bot.exit('%s must be type %s.' % (name, attr.attType))

    def load(self, content, validate=True):
        """given a dictionary load into its respective object
           if validate is True, we require it to be completely valid.
        """
        if not isinstance(content, dict):
            bot.exit('Please provide a dictionary or list to load.')
        lookup = self.generate_json_lookup()
        for key, value in content.items():
            att = lookup.get(key)
            if not att:
                bot.exit('%s is not a valid json attribute.' % key)

        self._clear_values()
        for key, value in content.items():
            att = lookup.get(key)
            valid = att.set(value)
            if valid or validate:
                bot.exit('%s (%s) is not valid.' % (att.name, att.jsonName))

        if validate:
            if not self.validate():
                bot.exit('%s is invalid' % self)
        return self

    def generate_json_lookup(self):
        """based on the attributes, generate a jsonName lookup object.
           keys are jsonNames we find in the wild, names are attribute names.
        """
        lookup = dict()
        for name, att in self.attrs.items():
            lookup[att.jsonName] = att

        return lookup

    def validate(self):
        """validate goes through each attribute, and ensure that it is of the
           correct type, and if required it is defined. This is already done
           to some extent when load is called, but this function serves as
           a final validation (after an initial config is loaded).
        """
        for name, att in self.attrs.items():
            if not att.required:
                if not att.value:
                    continue
                elif att.required:
                    att.value or bot.error('%s is required.' % name)
                    return False
                att.validate_type(att.value) or bot.error('%s should be type %s' % (name, att.attType))
                return False

        if hasattr(self, '_validate'):
            if not self._validate():
                return False
        return True


class StrStruct(Struct, str):
    __doc__ = "a string Struct provides (generally) the same functions, but isn't\n       tied to attributes but rather a single string value.\n    "

    def __init__(self, value, **kwargs):
        self.value = value or ''
        (super().__init__)(**kwargs)

    def load(self, content, validate=True):
        if isinstance(self, str):
            if isinstance(content, str):
                self = self.__class__(content)
                self.validate()
                return self


class IntStruct(Struct, int):
    __doc__ = "a string Struct provides (generally) the same functions, but isn't\n       tied to attributes but rather a single string value.\n    "

    def __init__(self, value, **kwargs):
        self.value = value or ''
        (super().__init__)(**kwargs)

    def load(self, content, validate=True):
        if isinstance(self, int):
            if isinstance(content, int):
                self = self.__class__(content)
                self.validate()
                return self