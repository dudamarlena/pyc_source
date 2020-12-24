# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/termine/gwexceptions.py
# Compiled at: 2012-07-17 09:23:20


class GWLoginException(BaseException):
    pass


class GWSessionException(BaseException):
    pass


class GWInitException(BaseException):
    pass


class GWConfigFileException(BaseException):
    pass


class GWFatalException(BaseException):
    pass


class GWItemFetchException(BaseException):
    pass


class GWForceLoginException(BaseException):
    pass


class GWBadArgumentException(BaseException):
    pass