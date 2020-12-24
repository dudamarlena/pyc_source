# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/kend/converter/base.py
# Compiled at: 2017-04-05 11:10:18
import exceptions

class ConversionError(exceptions.ValueError):
    pass


class NotImplementedError(ConversionError):
    """Raised when attempting to call an unimplemented converter method"""
    pass


class ParseError(ConversionError):
    """Raised when attempting to parse a format"""
    pass


class FormatError(ConversionError):
    """Raised when attempting to parse a format of the wrong schema"""
    pass


class VersionError(ConversionError):
    """Raised when attempting to parse a format of the wrong version"""
    pass


class SerialisationError(ConversionError):
    """Raised when attempting to serialise an incomplete object"""
    pass


class BaseConverter:

    @staticmethod
    def parse(*args, **kwargs):
        raise NotImplementedError()

    @staticmethod
    def serialise(*args, **kwargs):
        raise NotImplementedError()


class InvalidConverter:

    @staticmethod
    def parse(*args, **kwargs):
        raise ParseError('Unable to find parser for requested class (%s).' % str(args[0]))

    @staticmethod
    def serialise(*args, **kwargs):
        raise SerialisationError('Unable to find serialiser for requested class (%s).' % str(args[0]))


MIME_TYPE_BASE = 'application/x-kend'