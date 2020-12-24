# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Larco/Documents/Github/pyvenom/framework/venom/routing/Parameters.py
# Compiled at: 2016-04-26 14:29:46
import re, traceback
__all__ = [
 'Parameter', 'ChoicesParameter', 'String', 'Integer',
 'Float', 'Password', 'Dict', 'List', 'Model']

class ParameterValidationFailed(Exception):
    pass


class ParameterCastingFailed(Exception):
    pass


class Parameter(object):
    _attributes = [
     'required']
    _arguments = []
    required = True

    def __init__(self, required=True):
        super(Parameter, self).__init__()
        self.required = required

    def load(self, key, value):
        if value == None:
            if self.required:
                raise ParameterValidationFailed(("'{}' field was not found, but is required").format(key, value))
            return
        try:
            value = self.cast(key, value)
        except Exception as err:
            if isinstance(err, ParameterCastingFailed):
                raise
            traceback.print_exc()
            raise ParameterCastingFailed(("'{}' failed casting without specifying a reason").format(key))

        self.validate(key, value)
        return value

    def cast(self, key, value):
        return value

    def validate(self, key, value):
        pass

    def __iter__(self):
        cls = self.__class__
        yield ('type', cls.__name__)
        args = self._get_arguments_dict()
        for key, value in args.items():
            yield (
             key, value)

        yield ('attributes', self._get_attributes_dict())

    def __json__(self):
        return dict(self)

    def _get_attributes_dict(self):
        """
    ' Used by __repr__ and __iter__ to get all
    ' properties that should be represented as an attribute
    ' for this object. These are different than arguments.
    ' For example, a List template is an argument whereas
    ' required=False is an attribute.
    """
        attrs = {}
        for attribute in self._attributes:
            if hasattr(self, attribute):
                value = getattr(self, attribute)
                value = self._recursive_to_dict(value)
                attrs[attribute] = value

        return attrs

    def _get_arguments_dict(self):
        """
    ' Used by __repr__ and __iter__ to get all
    ' properties that should be represented at a root
    ' level of this object. These are different than attributes.
    ' For example, a List template is an argument whereas
    ' required=False is an attribute.
    """
        args = {}
        for argument in self._arguments:
            if hasattr(self, argument):
                value = getattr(self, argument)
                value = self._recursive_to_dict(value)
                args[argument] = value

        return args

    def _recursive_to_dict(self, value):
        if isinstance(value, Parameter):
            value = dict(value)
        elif isinstance(value, list):
            value = map(self._recursive_to_dict, value)
        elif isinstance(value, dict):
            value = {key:self._recursive_to_dict(val) for key, val in value.items()}
        return value

    def __repr__(self):
        cls = self.__class__
        attributes = set(self._attributes + self._arguments)
        args = []
        for attr in attributes:
            if hasattr(self, attr):
                value = getattr(self, attr)
                if not value == getattr(cls, attr):
                    args.append(('{}={!r}').format(attr, value))

        name = cls.__name__
        if not name.endswith('Parameter'):
            name += 'Parameter'
        return ('{}({})').format(name, (', ').join(args))


class ChoicesParameter(Parameter):
    _attributes = Parameter._attributes + ['choices']
    _arguments = Parameter._arguments
    choices = None

    def __init__(self, required=True, choices=None):
        super(ChoicesParameter, self).__init__(required=required)
        self.choices = choices

    def validate(self, key, value):
        super(ChoicesParameter, self).validate(key, value)
        self._validate_choices(key, value)

    def _validate_choices(self, key, value):
        if self.choices == None:
            return
        else:
            if value not in self.choices:
                raise ParameterValidationFailed(("'{}' field must be one of {} but instead it was '{}'").format(key, self.choices, value))
            return


class String(ChoicesParameter):
    _attributes = ChoicesParameter._attributes + ['min', 'max', 'characters', 'pattern']
    _arguments = ChoicesParameter._arguments
    min = None
    max = None
    characters = None
    pattern = None

    def __init__(self, required=True, choices=None, min=None, max=None, characters=None, pattern=None):
        super(String, self).__init__(required=required, choices=choices)
        self.min = min
        self.max = max
        self.characters = characters
        self.pattern = self._sanitize_pattern(pattern)

    def _sanitize_pattern(self, pattern):
        if not pattern:
            return None
        else:
            if not pattern.startswith('^'):
                pattern = ('^{}').format(pattern)
            if not pattern.endswith('$'):
                pattern = ('{}$').format(pattern)
            return pattern

    def cast(self, key, value):
        return str(value)

    def validate(self, key, value):
        super(String, self).validate(key, value)
        self._validate_min(key, value)
        self._validate_max(key, value)
        self._validate_characters(key, value)
        self._validate_pattern(key, value)

    def _validate_min(self, key, value):
        if self.min == None:
            return
        else:
            if len(value) < self.min:
                raise ParameterValidationFailed(("'{}' field requires at least {} characters but was provided '{}' of length {}").format(key, self.min, value, len(value)))
            return

    def _validate_max(self, key, value):
        if self.max == None:
            return
        else:
            if len(value) > self.max:
                raise ParameterValidationFailed(("'{}' field requires at most {} characters but was provided '{}' of length {}").format(key, self.max, value, len(value)))
            return

    def _validate_characters(self, key, value):
        if self.characters == None:
            return
        else:
            difference = set(value) - set(self.characters)
            if len(difference) > 0:
                raise ParameterValidationFailed(("'{}' field can only contain characters from '{}' but found characters from '{}'").format(key, ('').join(self.characters), ('').join(difference)))
            return

    def _validate_pattern(self, key, value):
        if self.pattern == None:
            return
        else:
            if not re.match(self.pattern, value):
                raise ParameterValidationFailed(("'{}' field must match pattern '{}' but was given '{}'").format(key, self.pattern, value))
            return


class Integer(ChoicesParameter):
    _attributes = ChoicesParameter._attributes + ['min', 'max']
    _arguments = ChoicesParameter._arguments
    min = None
    max = None

    def __init__(self, required=True, choices=None, min=None, max=None):
        super(Integer, self).__init__(required=required, choices=choices)
        self.min = min
        self.max = max

    def cast(self, key, value):
        return int(value)

    def validate(self, key, value):
        super(Integer, self).validate(key, value)
        self._validate_min(key, value)
        self._validate_max(key, value)

    def _validate_min(self, key, value):
        if self.min == None:
            return
        else:
            if value < self.min:
                raise ParameterValidationFailed(("'{}' field must be at least {} but was {}").format(key, self.min, value))
            return

    def _validate_max(self, key, value):
        if self.max == None:
            return
        else:
            if value > self.max:
                raise ParameterValidationFailed(("'{}' field must be at most {} but was {}").format(key, self.max, value))
            return


class Float(Integer):

    def cast(self, key, value):
        return float(value)


class Dict(Parameter):
    _attributes = Parameter._attributes
    _arguments = Parameter._arguments + ['template']
    template = None

    def __init__(self, template, required=True):
        super(Dict, self).__init__(required=required)
        self.template = self._sanitize_template(template)

    def _sanitize_template(self, template):
        if not isinstance(template, dict):
            raise Exception('Dict template must be a dict instance')
        for key, value in template.items():
            if isinstance(value, dict):
                template[key] = Dict(value)

        return template

    def cast(self, key, value):
        return dict(value)

    def validate(self, key, value):
        super(Dict, self).validate(key, value)
        self._validate_template(key, value)

    def _validate_template(self, root_key, value):
        for key, param in self.template.items():
            if not isinstance(param, Parameter):
                continue
            param_value = value[key] if key in value else None
            value[key] = param.load(('{}.{}').format(root_key, key), param_value)

        return


class List(Parameter):
    _attributes = Parameter._attributes + ['min', 'max']
    _arguments = Parameter._arguments + ['template']
    min = None
    max = None
    template = None

    def __init__(self, template, required=True, min=None, max=None):
        super(List, self).__init__(required=required)
        self.template = self._sanitize_template(template)
        self.min = min
        self.max = max

    def _sanitize_template(self, template):
        if isinstance(template, dict):
            return Dict(template)
        if not isinstance(template, Parameter):
            raise Exception('List template must be a dict or Parameter instance')
        return template

    def cast(self, key, value):
        return list(value)

    def validate(self, key, value):
        super(List, self).validate(key, value)
        self._validate_min(key, value)
        self._validate_max(key, value)
        self._validate_template(key, value)

    def _validate_template(self, root_key, value):
        for i, item in enumerate(value):
            value[i] = self.template.load(('{}[{}]').format(root_key, i), item)

    def _validate_min(self, key, value):
        if self.min == None:
            return
        else:
            if len(value) < self.min:
                raise ParameterValidationFailed(("'{}' field's length must be at least {} but was {}").format(key, self.min, len(value)))
            return

    def _validate_max(self, key, value):
        if self.max == None:
            return
        else:
            if len(value) > self.max:
                raise ParameterValidationFailed(("'{}' field's length must be at most {} but was {}").format(key, self.max, len(value)))
            return


class Model(Parameter):
    _attributes = Parameter._attributes
    _arguments = Parameter._arguments + ['modelname']

    def __init__(self, model, required=True):
        super(Model, self).__init__(required=required)
        self.model = model
        self.modelname = model.__name__

    def cast(self, key, value):
        value = super(Model, self).cast(key, value)
        return self.model.get(value)

    def validate(self, key, value):
        super(Model, self).validate(key, value)
        if not value:
            raise ParameterValidationFailed(("'{}' field found no entity from model {} matching the provided key").format(key, self.model.kind))