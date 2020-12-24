# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/rds/parametergroup.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 7037 bytes


class ParameterGroup(dict):

    def __init__(self, connection=None):
        dict.__init__(self)
        self.connection = connection
        self.name = None
        self.description = None
        self.engine = None
        self._current_param = None

    def __repr__(self):
        return 'ParameterGroup:%s' % self.name

    def startElement(self, name, attrs, connection):
        if name == 'Parameter':
            if self._current_param:
                self[self._current_param.name] = self._current_param
            self._current_param = Parameter(self)
            return self._current_param

    def endElement(self, name, value, connection):
        if name == 'DBParameterGroupName':
            self.name = value
        else:
            if name == 'Description':
                self.description = value
            else:
                if name == 'Engine':
                    self.engine = value
                else:
                    setattr(self, name, value)

    def modifiable(self):
        mod = []
        for key in self:
            p = self[key]
            if p.is_modifiable:
                mod.append(p)
                continue

        return mod

    def get_params(self):
        pg = self.connection.get_all_dbparameters(self.name)
        self.update(pg)

    def add_param(self, name, value, apply_method):
        param = Parameter()
        param.name = name
        param.value = value
        param.apply_method = apply_method
        self.params.append(param)


class Parameter(object):
    """Parameter"""
    ValidTypes = {'integer': int,  'string': str, 
     'boolean': bool}
    ValidSources = ['user', 'system', 'engine-default']
    ValidApplyTypes = ['static', 'dynamic']
    ValidApplyMethods = ['immediate', 'pending-reboot']

    def __init__(self, group=None, name=None):
        self.group = group
        self.name = name
        self._value = None
        self.type = 'string'
        self.source = None
        self.is_modifiable = True
        self.description = None
        self.apply_method = None
        self.allowed_values = None

    def __repr__(self):
        return 'Parameter:%s' % self.name

    def startElement(self, name, attrs, connection):
        pass

    def endElement(self, name, value, connection):
        if name == 'ParameterName':
            self.name = value
        else:
            if name == 'ParameterValue':
                self._value = value
            else:
                if name == 'DataType':
                    if value in self.ValidTypes:
                        self.type = value
                else:
                    if name == 'Source':
                        if value in self.ValidSources:
                            self.source = value
                    else:
                        if name == 'IsModifiable':
                            if value.lower() == 'true':
                                self.is_modifiable = True
                            else:
                                self.is_modifiable = False
                        else:
                            if name == 'Description':
                                self.description = value
                            else:
                                if name == 'ApplyType':
                                    if value in self.ValidApplyTypes:
                                        self.apply_type = value
                                else:
                                    if name == 'AllowedValues':
                                        self.allowed_values = value
                                    else:
                                        setattr(self, name, value)

    def merge(self, d, i):
        prefix = 'Parameters.member.%d.' % i
        if self.name:
            d[prefix + 'ParameterName'] = self.name
        if self._value is not None:
            d[prefix + 'ParameterValue'] = self._value
        if self.apply_type:
            d[prefix + 'ApplyMethod'] = self.apply_method

    def _set_string_value(self, value):
        if not isinstance(value, basestring):
            raise ValueError('value must be of type str')
        if self.allowed_values:
            choices = self.allowed_values.split(',')
            if value not in choices:
                raise ValueError('value must be in %s' % self.allowed_values)
        self._value = value

    def _set_integer_value(self, value):
        if isinstance(value, basestring):
            value = int(value)
        if isinstance(value, int) or isinstance(value, long):
            if self.allowed_values:
                min, max = self.allowed_values.split('-')
                if value < int(min) or value > int(max):
                    raise ValueError('range is %s' % self.allowed_values)
                self._value = value
        else:
            raise ValueError('value must be integer')

    def _set_boolean_value(self, value):
        if isinstance(value, bool):
            self._value = value
        else:
            if isinstance(value, basestring):
                if value.lower() == 'true':
                    self._value = True
                else:
                    self._value = False
            else:
                raise ValueError('value must be boolean')

    def set_value(self, value):
        if self.type == 'string':
            self._set_string_value(value)
        else:
            if self.type == 'integer':
                self._set_integer_value(value)
            else:
                if self.type == 'boolean':
                    self._set_boolean_value(value)
                else:
                    raise TypeError('unknown type (%s)' % self.type)

    def get_value(self):
        if self._value is None:
            return self._value
        if self.type == 'string':
            return self._value
        if self.type == 'integer':
            if not isinstance(self._value, int) and not isinstance(self._value, long):
                self._set_integer_value(self._value)
            return self._value
        if self.type == 'boolean':
            if not isinstance(self._value, bool):
                self._set_boolean_value(self._value)
            return self._value
        raise TypeError('unknown type (%s)' % self.type)

    value = property(get_value, set_value, 'The value of the parameter')

    def apply(self, immediate=False):
        if immediate:
            self.apply_method = 'immediate'
        else:
            self.apply_method = 'pending-reboot'
        self.group.connection.modify_parameter_group(self.group.name, [self])