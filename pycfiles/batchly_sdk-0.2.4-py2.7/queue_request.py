# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\batchly_sdk\request\queue_request.py
# Compiled at: 2015-09-28 08:57:26
from irequest import IRequest

class QueueRequest(IRequest):
    """
        QueueRequest is a type of request that supports pub/sub or queue sources
        Request holds the content of a single message
    """

    def __init__(self, id, content_path, parameters, content):
        self._content = content
        super(QueueRequest, self).__init__(id, content_path, parameters)

    @property
    def content(self):
        """
            Message content.

            Type: String
        """
        return self._content