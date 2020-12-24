# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/aeolus/exceptions.py
# Compiled at: 2020-01-07 11:45:47
# Size of source mod 2**32: 1191 bytes
__doc__ = 'Exceptions specific to aeolus package.'

class AeolusWarning(UserWarning):
    """AeolusWarning"""
    pass


class DeprecatedWarning(AeolusWarning):
    """DeprecatedWarning"""
    pass


class AeolusError(Exception):
    """AeolusError"""
    pass


class NotYetImplementedError(AeolusError):
    """NotYetImplementedError"""
    pass


class ArgumentError(AeolusError):
    """ArgumentError"""
    pass


class LoadError(AeolusError):
    """LoadError"""
    pass


class BoundaryError(AeolusError):
    """BoundaryError"""
    pass


class NotFoundError(AeolusError):
    """NotFoundError"""
    pass


class UnitFormatError(AeolusError):
    """UnitFormatError"""
    pass


class MissingCubeError(AeolusError):
    """MissingCubeError"""
    pass