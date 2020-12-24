# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/marathon_async/exceptions.py
# Compiled at: 2017-10-29 16:51:33
# Size of source mod 2**32: 662 bytes
from marathon.exceptions import MarathonError

class MarathonAioHttpError(MarathonError):

    def __init__(self, response, content=None):
        self.error_message = response.reason or ''
        if content:
            self.error_message = content.get('message', self.error_message)
            self.error_details = content.get('details')
        self.status_code = response.status
        super(MarathonAioHttpError, self).__init__(self.__str__())

    def __repr__(self):
        return 'MarathonHttpError: HTTP %s returned with message, "%s"' % (
         self.status_code, self.error_message)

    def __str__(self):
        return self.__repr__()