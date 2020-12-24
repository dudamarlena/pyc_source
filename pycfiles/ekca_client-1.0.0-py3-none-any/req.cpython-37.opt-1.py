# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /ekca_client/req.py
# Compiled at: 2019-11-06 02:51:49
# Size of source mod 2**32: 1677 bytes
"""
client for EKCA service -- JSON API requests
"""
import json, urllib.request
JSON_MEDIA_TYPE = 'application/json'
__all__ = [
 'EKCARequest',
 'EKCAUserCertRequest']

class EKCARequest(object):
    __doc__ = '\n    base class for request sent to EKCA service\n    '
    url_format = '{baseurl}/{ca_name}'
    method = 'POST'
    http_headers = {'Accept':JSON_MEDIA_TYPE, 
     'Content-type':JSON_MEDIA_TYPE}

    def __init__(self, base_url, ca_name, **payload):
        if base_url.endswith('/'):
            base_url = base_url[:-1]
        if ca_name:
            base_url = '{base_url}/{ca_name}'.format(base_url=base_url, ca_name=ca_name)
        if base_url.endswith('/'):
            base_url = base_url[:-1]
        self._base_url = base_url
        self._payload = payload

    @property
    def _req_url(self):
        return self.url_format.format(baseurl=(self._base_url))

    def req(self, cafile=None):
        """
        actually send the request
        """
        http_req = urllib.request.Request((self._req_url),
          data=(json.dumps(self._payload).encode('utf-8')),
          headers=(self.http_headers),
          origin_req_host=None,
          unverifiable=False,
          method=(self.method))
        return urllib.request.urlopen(http_req, cafile=cafile)


class EKCAUserCertRequest(EKCARequest):
    __doc__ = '\n    class for user certificate request sent to EKCA service\n    '
    url_format = '{baseurl}/usercert'