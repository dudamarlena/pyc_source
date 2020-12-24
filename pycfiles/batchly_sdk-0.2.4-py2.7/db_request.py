# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\batchly_sdk\request\db_request.py
# Compiled at: 2015-09-28 08:56:50
from irequest import IRequest

class DbRequest(IRequest):
    """
          DbRequest is a type of request that supports relational data sources
          Request holds the base data and source connection string
    """

    def __init__(self, id, content_path, parameters, connection_string, data):
        self._connection_string = connection_string
        self._data = data
        super(DbRequest, self).__init__(id, content_path, parameters)

    @property
    def connection_string(self):
        """
            Connection string from where data was read.

            Type: String
        """
        return self._connection_string

    @property
    def data(self):
        """
            Dictionary of data that was retrieved for this unit of work

            Type: Dictionary
        """
        return self._data