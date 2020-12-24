# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./guild/external/pip/_vendor/urllib3/util/response.py
# Compiled at: 2019-09-10 15:18:29
from __future__ import absolute_import
from ..packages.six.moves import http_client as httplib
from ..exceptions import HeaderParsingError

def is_fp_closed(obj):
    """
    Checks whether a given file-like object is closed.

    :param obj:
        The file-like object to check.
    """
    try:
        return obj.isclosed()
    except AttributeError:
        pass

    try:
        return obj.closed
    except AttributeError:
        pass

    try:
        return obj.fp is None
    except AttributeError:
        pass

    raise ValueError('Unable to determine whether fp is closed.')
    return


def assert_header_parsing(headers):
    """
    Asserts whether all headers have been successfully parsed.
    Extracts encountered errors from the result of parsing headers.

    Only works on Python 3.

    :param headers: Headers to verify.
    :type headers: `httplib.HTTPMessage`.

    :raises urllib3.exceptions.HeaderParsingError:
        If parsing errors are found.
    """
    if not isinstance(headers, httplib.HTTPMessage):
        raise TypeError(('expected httplib.Message, got {0}.').format(type(headers)))
    defects = getattr(headers, 'defects', None)
    get_payload = getattr(headers, 'get_payload', None)
    unparsed_data = None
    if get_payload:
        unparsed_data = get_payload()
    if defects or unparsed_data:
        raise HeaderParsingError(defects=defects, unparsed_data=unparsed_data)
    return


def is_response_to_head(response):
    """
    Checks whether the request of a response has been a HEAD-request.
    Handles the quirks of AppEngine.

    :param conn:
    :type conn: :class:`httplib.HTTPResponse`
    """
    method = response._method
    if isinstance(method, int):
        return method == 3
    return method.upper() == 'HEAD'