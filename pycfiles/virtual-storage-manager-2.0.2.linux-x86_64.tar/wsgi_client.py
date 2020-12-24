# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/manifest/wsgi_client.py
# Compiled at: 2016-06-13 14:11:03
"""
Use socket to transfer msg.
"""
import json, urllib2
from vsm import flags
from vsm.openstack.common import log as logging
from vsm import utils
import token
LOG = logging.getLogger(__name__)
FLAGS = flags.FLAGS

class WSGIClient(object):
    """WSGI Client service to get data from vsm-api.

    When used by vsm-agen, the password is get from server.manifest.
    """

    def __init__(self, vsm_api_ip='vsm_api_ip', info='token-tenantid'):
        """Initialized the url requestion and RUL."""
        self._vsm_api_ip = vsm_api_ip
        self._token = ('-').join(info.split('-')[0:-1])
        self._tenant_id = info.split('-')[(-1)]
        self._vsm_url = 'http://%s:%s/v1/%s' % (
         self._vsm_api_ip,
         8778,
         self._tenant_id)
        LOG.info('Agent token = %s, access url = %s' % (
         self._token, self._vsm_url))

    def index(self):
        """Use this method to get cluster's critial information."""
        req_url = self._vsm_url + '/agents'
        req = urllib2.Request(req_url)
        req.get_method = lambda : 'GET'
        req.add_header('content-type', 'application/json')
        req.add_header('X-Auth-Token', self._token)
        resp = urllib2.urlopen(req)
        recive_data = json.loads(resp.read())
        return recive_data

    def send(self, data, method, url='agents'):
        """Use parameter to contruct wsgi request to server.

        Below is an example how to send wsgi request to vsm-api server.

            url = "http://%(host)s:%(port)s/gw/%(id)/agents"
            req = urllib2.Request(url,
                  data=json.dumps({"agent":{"name":"test"}}))
            req.get_method = lambda: "POST"
            req.add_header("content-type", "application/json")
            resp = urllib2.urlopen(req)
            configs = json.loads(resp.read())

        It's easy to transfer %(id), for simple, you can juse transfer 1.
        """
        pass