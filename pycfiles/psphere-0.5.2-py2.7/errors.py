# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/psphere/errors.py
# Compiled at: 2013-02-21 17:34:08


class ConfigError(Exception):
    pass


class NotLoggedInError(Exception):
    pass


class ObjectNotFoundError(Exception):
    pass


class TaskFailedError(Exception):
    pass


class TemplateNotFoundError(Exception):
    pass


class NotImplementedError(Exception):
    pass