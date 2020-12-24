# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/e24PaymentPipe/exceptions.py
# Compiled at: 2015-12-29 16:07:46
__author__ = 'burhan'

class ErrorUrlMissing(Exception):
    pass


class ResponseUrlMissing(Exception):
    pass


class AmountGreaterThanZero(Exception):
    pass


class GatewayError(Exception):
    pass