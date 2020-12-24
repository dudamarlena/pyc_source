# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/http/spec/codes.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Jun 30, 2011

@package: ally http
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Contains the codes to be used for the server responses.
"""
from ally.support.util import tupleify

@tupleify('code', 'status', 'isSuccess')
class CodeHTTP:
    """
    Contains the HTTP response code.
    """

    def __init__(self, code, status, isSuccess):
        """
        Constructs the code.
        
        @param code: string
            The code text corresponding to this code.
        @param status: integer
            The HTTP status code.
        @param isSuccess: boolean
            Flag indicating if the code is a fail or success code.
        """
        assert isinstance(code, str), 'Invalid code %s' % code
        assert isinstance(status, int), 'Invalid status %s' % status
        assert isinstance(isSuccess, bool), 'Invalid success flag %s' % isSuccess
        self.code = code
        self.status = status
        self.isSuccess = isSuccess


def isSuccess(status):
    """
    Checks if the status provided is a success status.
    
    @param status: integer
        The status code to check if is for a successful operation.
    @return: boolean
        True if the status is a success status, False otherwise.
    """
    assert isinstance(status, int), 'Invalid status %s' % status
    return status / 100 == 2


PATH_NOT_FOUND = CodeHTTP('Not found', 404, False)
PATH_FOUND = CodeHTTP('OK', 200, True)
METHOD_NOT_AVAILABLE = CodeHTTP('Method not allowed', 405, False)
BAD_REQUEST = CodeHTTP('Bad Request', 400, False)
HEADER_ERROR = CodeHTTP('Invalid header', 400, False)
INTERNAL_ERROR = CodeHTTP('Internal error', 500, False)
SERVICE_UNAVAILABLE = CodeHTTP('Service Unavailable', 503, False)
BAD_GATEWAY = CodeHTTP('Bad Gateway', 502, False)
UNAUTHORIZED_ACCESS = CodeHTTP('Unauthorized access', 401, False)
INVALID_AUTHORIZATION = CodeHTTP('Invalid authorization', 401, False)
FORBIDDEN_ACCESS = CodeHTTP('Forbidden access', 403, False)