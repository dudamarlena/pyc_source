# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/users/cpt/cpt/esr/Projects/galaxy/galaxygetopt/env/lib/python2.7/site-packages/galaxygetopt/exceptions.py
# Compiled at: 2014-07-07 15:44:50


class ParameterValidationError(Exception):
    pass


class UnknownRequestedOutputFileError(Exception):
    pass


class UnspecifiedGGOObjectError(Exception):
    pass


class UnspecifiedOutputFileError(Exception):
    pass


class UnacceptableOutputFormatError(Exception):
    pass


class NoAvailableOutputHandlerError(Exception):
    pass


class UnknownStrategyError(Exception):
    pass


class AuthorParameterSpecificationError(Exception):
    pass


class WriterProcessingIncompleteError(Exception):
    pass


class UnimplementedException(Exception):
    """Maybe this should email me?"""
    pass


class RepeatRequestedFromNonMultiple(Exception):
    pass


class UnknownDataHandlerException(Exception):
    pass


class UnknownDataFormatException(Exception):
    pass