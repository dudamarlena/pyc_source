# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/coded_exceptions.py
# Compiled at: 2011-04-30 07:47:24
"""
Module provides new base class for exceptions: CodedException.

Each subclass of CodedException have unique attribute 'code'.
If code is unspecified, it will be generated from class name
(see CodedExceptionMeta.make_code_from_name for details).

Unique constraint is controlled at the class creation time. If
exception class with same code was already defined somewhere and
thus registered in CodedExceptionMeta._registered_exceptions,
CodedExceptionExists will be raised.
"""
import re

class CodedExceptionExists(Exception):
    pass


class CodedExceptionMeta(type):
    _registered_exceptions = {}

    def __new__(cls, name, bases, attrs):
        new_class = super(CodedExceptionMeta, cls).__new__(cls, name, bases, attrs)
        if bases[0] != Exception or len(bases) != 1:
            if 'code' in attrs:
                code = attrs['code']
                if code is not None:
                    cls.set_code_or_die(code, new_class)
            else:
                code = cls.make_code_from_name(name)
                new_class.code = code
                cls.set_code_or_die(code, new_class)
        return new_class

    @classmethod
    def set_code_or_die(cls, code, new_class):
        old_class = cls._registered_exceptions.setdefault(code, new_class)
        if old_class is not new_class:
            raise CodedExceptionExists(code, old_class, new_class)

    @staticmethod
    def make_code_from_name(name):
        """
        Default code inducer.

        Example:
        >>> CodedExceptionMeta.make_code_from_name('SomeCustomValidationError')
        'some_custom_validation_error'
        """
        canonical_name = re.sub('([a-z])([A-Z])', '\\1_\\2', name).lower()
        return canonical_name


class CodedException(Exception):
    __metaclass__ = CodedExceptionMeta
    code = 0
    context = None
    text_message = None