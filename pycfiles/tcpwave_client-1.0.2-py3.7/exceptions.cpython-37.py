# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tcpwave_client/exceptions.py
# Compiled at: 2020-04-13 11:17:12
# Size of source mod 2**32: 459 bytes


class IPAMException(Exception):

    def __init__(self, msg):
        super(IPAMException, self).__init__(msg)
        self.msg = msg


class APICallFailedException(IPAMException):

    def __init__(self, msg):
        super(APICallFailedException, self).__init__(msg)
        self.msg = msg


class UnsupportedMethodException(IPAMException):

    def __init__(self, msg):
        super(UnsupportedMethodException, self).__init__(msg)
        self.msg = msg