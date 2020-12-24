# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-uunam8sj/pip/pip/_internal/network/xmlrpc.py
# Compiled at: 2020-03-25 22:23:37
# Size of source mod 2**32: 1597 bytes
"""xmlrpclib.Transport implementation
"""
import logging
from pip._vendor import requests
from pip._vendor.six.moves import xmlrpc_client
from pip._vendor.six.moves.urllib import parse as urllib_parse
logger = logging.getLogger(__name__)

class PipXmlrpcTransport(xmlrpc_client.Transport):
    __doc__ = 'Provide a `xmlrpclib.Transport` implementation via a `PipSession`\n    object.\n    '

    def __init__(self, index_url, session, use_datetime=False):
        xmlrpc_client.Transport.__init__(self, use_datetime)
        index_parts = urllib_parse.urlparse(index_url)
        self._scheme = index_parts.scheme
        self._session = session

    def request(self, host, handler, request_body, verbose=False):
        parts = (
         self._scheme, host, handler, None, None, None)
        url = urllib_parse.urlunparse(parts)
        try:
            headers = {'Content-Type': 'text/xml'}
            response = self._session.post(url, data=request_body, headers=headers,
              stream=True)
            response.raise_for_status()
            self.verbose = verbose
            return self.parse_response(response.raw)
        except requests.HTTPError as exc:
            logger.critical('HTTP error %s while getting %s', exc.response.status_code, url)
            raise