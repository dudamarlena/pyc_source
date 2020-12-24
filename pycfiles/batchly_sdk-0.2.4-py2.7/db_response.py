# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\batchly_sdk\response\db_response.py
# Compiled at: 2015-09-28 09:08:47
from iresponse import IResponse

class DbResponse(IResponse):
    """
        Use this response type when you want batchly a execute a query on completion of the processing.
        The parameter_values is a dictionary which can contain the name and values for each parameter of your configured query
    """

    def __init__(self, request, parameter_values=None):
        self._parameter_values = parameter_values
        super(DbResponse, self).__init__(request)

    @property
    def parameter_values(self):
        return self._parameter_values

    @parameter_values.setter
    def parameter_values(self, value):
        """
            Dictionary of data that wil be used to update the paramters of db query

            Type: Dictionary
        """
        self._parameter_values = value