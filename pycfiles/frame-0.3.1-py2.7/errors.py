# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/frame/orm/errors.py
# Compiled at: 2013-02-17 12:08:22


class ValidateError(Exception):
    pass


class RequiredFieldError(ValidateError):
    pass


class ExtraFieldError(ValidateError):
    pass


class ModelLoadError(Exception):
    pass