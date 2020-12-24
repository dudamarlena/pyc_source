# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyjon/descriptors/exceptions.py
# Compiled at: 2015-01-20 10:16:16
"""Exceptions that can be raised by the descriptors when running
"""

class DescriptorError(Exception):
    """
    base exception for all descriptor errors
    """
    pass


class ConstraintError(DescriptorError):
    """
    all length or mandatory/missing errors should use this base exception
    """
    pass


class InvalidDescriptorError(DescriptorError):
    """
    the descriptor is invalid, fix it
    """
    pass


class MaxLenError(ConstraintError):
    """
    a field max len has not been respected
    """
    pass


class MinLenError(ConstraintError):
    """
    a field min len has not been respected
    """
    pass


class MissingFieldError(ConstraintError):
    """
    when a field is declared mandatory in the xml descriptor and is not
    present in the source then the descriptor will raise this exception
    """
    pass


class SourceError(ConstraintError):
    """
    when a line in the source as more or less columns than
    what we excpect
    """
    pass


class TooManyFieldsError(SourceError):
    """when a 'line' has too many fields
    """
    pass


class TooFewFieldsError(SourceError):
    """when a 'line' has too few fields
    """
    pass


class RemainingDataError(SourceError):
    """
    if xml source contains data after last rc closing tag and this
    data contains tags like it or rc.
    """
    pass