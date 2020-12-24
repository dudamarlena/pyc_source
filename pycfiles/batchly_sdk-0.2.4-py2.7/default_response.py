# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\batchly_sdk\response\default_response.py
# Compiled at: 2015-09-28 08:59:00
from iresponse import IResponse

class DefaultResponse(IResponse):
    """
        Use this response type when no post processing is required to be done by
        Batchly. Creating this DefaultResponse automatically updates the success
        state of the response.

        For explicitly setting the success as False or for marking this request
        as a duplicate request, you can set the is_processing_success or is_duplicate
        properties with the appropriate values
    """

    def __init__(self, request):
        super(DefaultResponse, self).__init__(request)