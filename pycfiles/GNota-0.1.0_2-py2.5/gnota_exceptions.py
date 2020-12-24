# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/GNota/gnota_exceptions.py
# Compiled at: 2007-08-17 04:25:25


class GNotaException(Exception):
    pass


class NoSuchGradeException(GNotaException):
    pass


class NoSuchClassException(GNotaException):
    pass


class NoSuchScoreSystemException(GNotaException):
    pass


class ScoresystemException(GNotaException):
    pass


class GNotaDatabaseInconsistencyException(GNotaException):
    pass


class GNotaTypeException(GNotaException):
    pass


class NoSelectedClassException(GNotaException):
    pass


class GNotaConversionException(GNotaException):
    pass


class CategoryWithNoWeightException(GNotaException):
    pass