# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/prompt_tool_kit/validation.py
# Compiled at: 2019-08-15 23:53:38
# Size of source mod 2**32: 1756 bytes
__doc__ = '\nInput validation for a `Buffer`.\n(Validators will be called before accepting input.)\n'
from __future__ import unicode_literals
from .filters import to_simple_filter
from abc import ABCMeta, abstractmethod
from six import with_metaclass
__all__ = ('ConditionalValidator', 'ValidationError', 'Validator')

class ValidationError(Exception):
    """ValidationError"""

    def __init__(self, cursor_position=0, message=''):
        super(ValidationError, self).__init__(message)
        self.cursor_position = cursor_position
        self.message = message

    def __repr__(self):
        return '%s(cursor_position=%r, message=%r)' % (
         self.__class__.__name__, self.cursor_position, self.message)


class Validator(with_metaclass(ABCMeta, object)):
    """Validator"""

    @abstractmethod
    def validate(self, document):
        """
        Validate the input.
        If invalid, this should raise a :class:`.ValidationError`.

        :param document: :class:`~prompt_tool_kit.document.Document` instance.
        """
        pass


class ConditionalValidator(Validator):
    """ConditionalValidator"""

    def __init__(self, validator, filter):
        assert isinstance(validator, Validator)
        self.validator = validator
        self.filter = to_simple_filter(filter)

    def validate(self, document):
        if self.filter():
            self.validator.validate(document)