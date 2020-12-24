# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyjon/descriptors/exceptions.py
# Compiled at: 2015-01-20 10:16:16
__doc__ = 'Exceptions that can be raised by the descriptors when running\n'

class DescriptorError(Exception):
    """
    base exception for all descriptor errors
    """


class ConstraintError(DescriptorError):
    """
    all length or mandatory/missing errors should use this base exception
    """


class InvalidDescriptorError(DescriptorError):
    """
    the descriptor is invalid, fix it
    """


class MaxLenError(ConstraintError):
    """
    a field max len has not been respected
    """


class MinLenError(ConstraintError):
    """
    a field min len has not been respected
    """


class MissingFieldError(ConstraintError):
    """
    when a field is declared mandatory in the xml descriptor and is not
    present in the source then the descriptor will raise this exception
    """


class SourceError(ConstraintError):
    """
    when a line in the source as more or less columns than
    what we excpect
    """


class TooManyFieldsError(SourceError):
    """when a 'line' has too many fields
    """


class TooFewFieldsError(SourceError):
    """when a 'line' has too few fields
    """


class RemainingDataError(SourceError):
    """
    if xml source contains data after last rc closing tag and this
    data contains tags like it or rc.
    """