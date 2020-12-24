# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sigma/core/validator.py
# Compiled at: 2016-01-24 18:34:38
# Size of source mod 2**32: 1400 bytes
"""
"""
from functools import partial

class FieldValidator(object):
    __doc__ = '\n    '

    def __init__(self, field, *args, **kwargs):
        """
        Args:
          field: A Field instance.
          *args: A list of validate function names.
          **kwargs: Keyword arguments of the Field constructor.
            key: An option name
            value: An option setting value.
        """
        self.field = field
        self.args = args
        self.kwargs = kwargs
        validates = []
        for key in field.__order__:
            option = field.__options__[key]
            if key in kwargs:
                option.value = kwargs[key]
                validates.append(partial(option.func, field, option))
            elif hasattr(option, 'default'):
                option.value = option.default
                validates.append(partial(option.func, field, option))
            elif option.required or key in args:
                validates.append(partial(option.func, field, option))
                continue

        self.validates = validates

    def validate(self, value):
        """ Validate value.
        Args:
          value:
        Returns:
          A validated value.
        Raises:
          UnitError
        """
        for validate in self.validates:
            value = validate(value)

        return value