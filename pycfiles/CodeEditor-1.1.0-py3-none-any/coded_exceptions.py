# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/coded_exceptions.py
# Compiled at: 2011-04-30 07:47:24
__doc__ = "\nModule provides new base class for exceptions: CodedException.\n\nEach subclass of CodedException have unique attribute 'code'.\nIf code is unspecified, it will be generated from class name\n(see CodedExceptionMeta.make_code_from_name for details).\n\nUnique constraint is controlled at the class creation time. If\nexception class with same code was already defined somewhere and\nthus registered in CodedExceptionMeta._registered_exceptions,\nCodedExceptionExists will be raised.\n"
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