# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/finbull/error.py
# Compiled at: 2019-08-01 22:03:09
# Size of source mod 2**32: 1421 bytes
ERRNO_OK = 0
ERRMSG_OK = 'ok'
ERRNO_FRAMEWORK = 9999
ERRMSG_FRAMEWORK = 'the FinBull framework error'
ERRNO_UNKNOWN = 9998
ERRMSG_UNKNOWN = 'unknown error'
ERROR = {ERRNO_OK: ERRMSG_OK, 
 ERRNO_FRAMEWORK: ERRMSG_FRAMEWORK, 
 ERRNO_UNKNOWN: ERRMSG_UNKNOWN}

class BaseError(Exception):
    __doc__ = '\n    every Error should extend BaseError\n    '

    def __init__(self, errno=ERRNO_FRAMEWORK, errmsg=None):
        """
        check error or errmsg
        """
        if errno in ERROR:
            self.errno = errno
            if errmsg is None:
                self.errmsg = ERROR[errno]
            else:
                self.errmsg = errmsg
        else:
            self.errno = ERRNO_UNKNOWN
            if errmsg is None:
                self.errmsg = ERROR[ERRNO_UNKNOWN]
            else:
                self.errmsg = errmsg
        super(BaseError, self).__init__(errmsg)