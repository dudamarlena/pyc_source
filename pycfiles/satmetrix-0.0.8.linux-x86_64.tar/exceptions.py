# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/satmetrix/exceptions.py
# Compiled at: 2017-05-25 09:13:14


class SatmetrixAPIError(Exception):
    """Satmetrix Returned Error"""
    pass


class SatmetrixAPIErrorNotFound(SatmetrixAPIError):
    """Satmetrix Returned 4xx Error"""
    pass


class SatmetrixAPIErrorInternalError(SatmetrixAPIError):
    """Satmetrix Returned 5xx Error"""
    pass