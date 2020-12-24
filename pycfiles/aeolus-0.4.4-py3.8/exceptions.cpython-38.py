# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/aeolus/exceptions.py
# Compiled at: 2020-01-07 11:45:47
# Size of source mod 2**32: 1191 bytes
"""Exceptions specific to aeolus package."""

class AeolusWarning(UserWarning):
    __doc__ = 'Base class for warnings in aeolus package.'


class DeprecatedWarning(AeolusWarning):
    __doc__ = 'Warning for a deprecated feature.'


class AeolusError(Exception):
    __doc__ = 'Base class for errors in aeolus package.'


class NotYetImplementedError(AeolusError):
    __doc__ = '\n    Raised by missing functionality.\n\n    Different meaning to NotImplementedError, which is for abstract methods.\n    '


class ArgumentError(AeolusError):
    __doc__ = 'Raised when argument type is not recognised or is not allowed.'


class LoadError(AeolusError):
    __doc__ = 'Raised when input files or directories are not found.'


class BoundaryError(AeolusError):
    __doc__ = 'Raised when there is an error with geographical regions.'


class NotFoundError(AeolusError):
    __doc__ = 'Raised when metadata is not found.'


class UnitFormatError(AeolusError):
    __doc__ = 'Raised when cube units cannot be formatted.'


class MissingCubeError(AeolusError):
    __doc__ = 'Raised when cubes required for a calculation are missing.'