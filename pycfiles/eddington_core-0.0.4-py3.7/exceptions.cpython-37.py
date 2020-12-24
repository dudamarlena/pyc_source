# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eddington_core/exceptions.py
# Compiled at: 2020-04-04 11:50:41
# Size of source mod 2**32: 174 bytes


class EddingtonException(Exception):
    pass


class InvalidGeneratorInitialization(EddingtonException):
    pass


class FitFunctionLoadError(EddingtonException):
    pass