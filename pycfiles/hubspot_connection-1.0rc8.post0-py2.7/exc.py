# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hubspot/connection/exc.py
# Compiled at: 2016-08-16 04:41:21


class HubspotException(Exception):
    """The base HubSpot error."""
    pass


class HubspotUnsupportedResponseError(HubspotException):
    pass


class HubspotInvalidResponseError(HubspotException):

    def __init__(self):
        Exception.__init__(self, 'Invalid JSON response body')


class HubspotClientError(HubspotException):
    """
    HubSpot deemed the request invalid. This represents an HTTP response code
    of 40X, except 401

    :param unicode request_id:

    """

    def __init__(self, msg, request_id):
        super(HubspotClientError, self).__init__(msg)
        self.request_id = request_id


class HubspotAuthenticationError(HubspotClientError):
    """
    HubSpot rejected your authentication key. This represents an HTTP
    response code of 401.

    """
    pass


class HubspotServerError(HubspotException):
    """
    HubSpot failed to process the request due to a problem at their end. This
    represents an HTTP response code of 50X.

    :param int http_status_code:

    """

    def __init__(self, msg, http_status_code):
        super(HubspotServerError, self).__init__(msg)
        self.msg = msg
        self.http_status_code = http_status_code

    def __repr__(self):
        return ('{} {}').format(self.http_status_code, self.msg)