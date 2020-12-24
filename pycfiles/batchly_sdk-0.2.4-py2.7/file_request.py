# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\batchly_sdk\request\file_request.py
# Compiled at: 2015-09-28 16:35:49
from irequest import IRequest

class FileRequest(IRequest):
    """
        Use this request if you require the file to be available on local disk for processing.
        You can access the input file location using the Location property
    """

    def __init__(self, id, content_path, parameters, location):
        self._location = location
        super(FileRequest, self).__init__(id, content_path, parameters)

    @property
    def location(self):
        """
            Location of input file on local disk.

            Type: String
        """
        return self._location