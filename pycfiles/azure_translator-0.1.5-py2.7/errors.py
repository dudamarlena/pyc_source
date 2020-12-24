# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/azure_translator/errors.py
# Compiled at: 2017-02-15 19:19:52
"""Azure errors module."""
import xml.etree.ElementTree as ET

class BaseAzureException(Exception):
    """
    Base exception for the SDK.
    """

    def __init__(self, *args, **kwargs):
        self.response = kwargs.pop('response', None)
        self.request = kwargs.pop('request', None)
        super(BaseAzureException, self).__init__(*args, **kwargs)
        return


class AzureApiError(BaseAzureException):
    """
    Raised when the API returns a non-200 body.
    """
    MSG_SEPARATOR = '; '

    def __init__(self, msg, *args, **kwargs):
        response = kwargs.get('response')
        if response is not None:
            try:
                msg = ('HTTP status: {}; {}').format(response.status_code, self.MSG_SEPARATOR.join(ET.fromstring(response.content).itertext())).replace('\r\n', self.MSG_SEPARATOR)
            except ET.ParseError:
                pass

        super(AzureApiError, self).__init__(msg, *args, **kwargs)
        return


class AzureApiBadFormatError(BaseAzureException):
    """
    Raised when the API returns a malformed error.
    """
    pass


class AzureCannotGetTokenError(AzureApiError):
    """
    Raised when the API refuses to return a token.
    """
    pass


class AzureApiTimeoutError(BaseAzureException):
    """
    Raised when the API times out.
    """
    pass