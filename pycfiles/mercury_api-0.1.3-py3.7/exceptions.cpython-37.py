# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_api/exceptions.py
# Compiled at: 2018-06-20 15:42:58
# Size of source mod 2**32: 1130 bytes


class HTTPError(Exception):
    __doc__ = '\n    Generic exception to be used when raising http errors in the application\n    and transforms the message into a dictionary to be used by the app error\n    handler.\n    '

    def __init__(self, message, status_code=400):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        payload = {'error':True, 
         'message':self.message}
        return payload