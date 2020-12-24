# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bmeyer/Devel/stackInABox/.tox/twine/lib/python2.7/site-packages/stackinabox/util/responses/core.py
# Compiled at: 2017-05-27 01:24:11
"""
Stack-In-A-Box: Python Responses Support
"""
from __future__ import absolute_import
import logging, re, responses
from stackinabox.stack import StackInABox
from stackinabox.util.tools import CaseInsensitiveDict
logger = logging.getLogger(__name__)

def responses_callback(request):
    """Responses Request Handler.

    Converts a call intercepted by Responses to
    the Stack-In-A-Box infrastructure

    :param request: request object

    :returns: tuple - (int, dict, string) containing:
                      int - the HTTP response status code
                      dict - the headers for the HTTP response
                      string - HTTP string response
    """
    method = request.method
    headers = CaseInsensitiveDict()
    request_headers = CaseInsensitiveDict()
    request_headers.update(request.headers)
    request.headers = request_headers
    uri = request.url
    return StackInABox.call_into(method, request, uri, headers)


def responses_registration(uri):
    """Responses handler registration.

    Registers a handler for a given URI with Responses
    so that it can be intercepted and handed to
    Stack-In-A-Box.

    :param uri: URI used for the base of the HTTP requests

    :returns: n/a
    """
    logger.debug(('Registering Stack-In-A-Box at {0} under Python Responses').format(uri))
    StackInABox.update_uri(uri)
    regex = re.compile(('(http)?s?(://)?{0}:?(\\d+)?/').format(uri), re.I)
    METHODS = [
     responses.DELETE,
     responses.GET,
     responses.HEAD,
     responses.OPTIONS,
     responses.PATCH,
     responses.POST,
     responses.PUT]
    for method in METHODS:
        responses.add_callback(method, regex, callback=responses_callback)