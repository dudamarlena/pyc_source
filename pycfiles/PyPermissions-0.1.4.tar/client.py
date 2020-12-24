# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/pypermedia/client.py
# Compiled at: 2016-02-16 21:10:17
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import requests, requests.exceptions
from pypermedia.siren import SirenBuilder

class HypermediaClient(object):
    """
    Entry-point and helper methods for using the codex service. This performs the initial setup, all other client calls
    are created dynamically from service responses.
    """

    @staticmethod
    def connect(root_url, session=None, verify=False, request_factory=requests.Request, builder=SirenBuilder):
        """
        Creates a client by connecting to the root api url. Pointing to other urls is possible so long as their
        responses correspond to standard siren-json.

        :param str|unicode root_url: root api url
        :param bool verify: whether to verify ssl certificates from the server or ignore them (should be false for
            local dev)
        :param type|function request_factory: constructor of request objects
        :return: codex client generated from root url
        :rtype: object
        """
        request = request_factory(b'GET', root_url)
        p = request.prepare()
        return HypermediaClient.send_and_construct(p, session=session, verify=verify, request_factory=request_factory, builder=builder)

    @staticmethod
    def send_and_construct(prepared_request, session=None, verify=False, request_factory=requests.Request, builder=SirenBuilder):
        """
        Takes a PreparedRequest object and sends it and then constructs the SirenObject from the response.

        :param requests.PreparedRequest prepared_request: The initial request to send.
        :param requests.Session session : Existing session to use for requests.
        :param bool verify: whether to verify ssl certificates from the server or ignore them (should be false for
            local dev)
        :param type|function request_factory: constructor of request object
        :param builder:  The object to build the hypermedia object
        :return: The object representing the siren object returned from the server.
        :rtype: object
        :raises: ConnectError
        """
        session = session or requests.Session()
        try:
            response = session.send(prepared_request, verify=verify)
        except requests.exceptions.ConnectionError as e:
            raise ConnectError((b'Unable to connect to server! Unable to construct client. root_url="{0}" verify="{1}"').format(prepared_request.url, verify), e)

        builder = builder(verify=verify, request_factory=request_factory)
        obj = builder.from_api_response(response)
        return obj.as_python_object()


class ConnectError(Exception):
    """Standard error for an inability to connect to the server."""


class APIError(Exception):
    """Bucket for errors related to server responses."""