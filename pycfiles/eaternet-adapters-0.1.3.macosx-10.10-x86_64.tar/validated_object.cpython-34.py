# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robb/src/adapters-python/venv/lib/python3.4/site-packages/eaternet/lives_1_0/validated_object.py
# Compiled at: 2015-08-06 02:06:13
# Size of source mod 2**32: 4500 bytes
from collections import namedtuple
from eaternet.exceptions import ValidationError
OptionSet = namedtuple('OptionSet', ('minimum', 'maximum', 'inclusion_in', 'required',
                                     'validator', 'intended_class'))
Attribute = namedtuple('Attribute', ('name', 'val'))

class ValidatedObject:
    __doc__ = '\n    A small attribute validation framework\n\n    See entities.py\n    '

    def required(self, attr, attr_name, intended_class, validator=None, minimum=None, maximum=None, inclusion_in=None):
        """Declare a required attribute"""
        options = OptionSet(minimum, maximum, inclusion_in, True, validator, intended_class)
        attribute = Attribute(name=attr_name, val=attr)
        return self._add_validation(attribute, options)

    def optional(self, attr, attr_name, intended_class, validator=None, minimum=None, maximum=None, inclusion_in=None):
        """Declare an optional attribute"""
        options = OptionSet(minimum, maximum, inclusion_in, False, validator, intended_class)
        attribute = Attribute(name=attr_name, val=attr)
        return self._add_validation(attribute, options)

    def validate(self):
        """Raise a ValidationError if any validations failed"""
        if self._error_list():
            raise ValidationError('; '.join(self._error_list()))

    def _add_validation(self, attribute, options):
        """Validate and set the attribute"""
        if _should_validate(attribute.val, options):
            self._find_and_save_errors(attribute, options)
        setattr(self, attribute.name, attribute.val)
        return self

    def _find_and_save_errors(self, attribute, options):
        if self._save_error(_check_type(attribute, options.intended_class)):
            return
        checks = {_check_type: options.intended_class, 
         _check_inclusion: options.inclusion_in, 
         _check_maximum: options.maximum, 
         _check_minimum: options.minimum, 
         _check_is_blank: True, 
         _check_validator: options.validator}
        errors = self._run_selected(checks, attribute)

    def _run_selected(self, checks, attribute):
        for check, option in compact(checks).items():
            self._save_error(check(attribute, option))

    def _save_error(self, error_string):
        if error_string:
            self._error_list().append(error_string)
            return True

    def _error_list(self):
        """Lazily instantiate the errors array to enable a cleaner __init__()"""
        try:
            self._errors
        except AttributeError:
            self._errors = []

        return self._errors


def _check_type(attribute, intended_class):
    value = attribute.val
    if not isinstance(value, intended_class):
        return '{3} with value {0} is {1}, not {2}'.format(value, type(value), intended_class, attribute.name)


def _check_validator(attribute, validator):
    if not validator(attribute.val):
        return '{0} = {1} is invalid'.format(attribute.name, attribute.val)


def _check_is_blank(attribute, option):
    if is_blank(attribute.val):
        return '{0} is blank'.format(attribute.name)


def _check_minimum(attribute, minimum):
    if attribute.val < minimum:
        return '{0} = {1} which is < the minimum, {2}'.format(attribute.name, attribute.val, minimum)


def _check_maximum(attribute, maximum):
    if attribute.val > maximum:
        return '{0} = {1} which is > the maximum, {2}'.format(attribute.name, attribute.val, maximum)


def _check_inclusion(attribute, inclusion_in):
    if attribute.val not in inclusion_in:
        return '{0} = {1} which is not in {2}'.format(attribute.name, attribute.val, inclusion_in)


def is_blank(a_string):
    return type(a_string) is str and len(a_string) == 0


def compact(a_dict):
    return {k:v for k, v in a_dict.items() if v is not None if v is not None}


def _should_validate(obj, options):
    return options.required or obj is not None