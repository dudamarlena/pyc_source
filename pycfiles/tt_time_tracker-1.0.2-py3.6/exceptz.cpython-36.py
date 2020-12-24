# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tt/exceptz/exceptz.py
# Compiled at: 2020-03-10 16:51:28
# Size of source mod 2**32: 543 bytes


class TIError(Exception):
    __doc__ = 'Errors raised by TI.'


class AlreadyOn(TIError):
    __doc__ = 'Already working on that task.'


class NoEditor(TIError):
    __doc__ = 'No $EDITOR set.'


class InvalidYAML(TIError):
    __doc__ = 'No $EDITOR set.'


class NoTask(TIError):
    __doc__ = 'Not working on a task yet.'


class BadArguments(TIError):
    __doc__ = 'The command line arguments passed are not valid.'


class BadTime(TIError):
    __doc__ = "Time string can't be parsed."


class NonexistentDatasource(TIError):
    __doc__ = 'The requested datasource is not supported'