# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\batchly_sdk\request\delimited_file_request.py
# Compiled at: 2015-09-28 08:57:29
from irequest import IRequest

class DelimitedFileRequest(IRequest):
    """
        DelimitedFileRequest is a type of request that supports csv and other delmited type of source files
        Request holds the fields as an array.  The fields are column values from a single row

    """

    def __init__(self, id, content_path, parameters, fields):
        self._fields = fields
        super(DelimitedFileRequest, self).__init__(id, content_path, parameters)

    @property
    def fields(self):
        """
            Fields contain the individual columns of a delimited row

            Type: Array
        """
        return self._fields