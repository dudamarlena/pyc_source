# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flask_consulate/service.py
# Compiled at: 2017-04-16 13:46:21
# Size of source mod 2**32: 3681 bytes
import requests
from dns.resolver import Resolver
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin

from flask_consulate.decorators import with_retry_connections

class ConsulService(object):
    __doc__ = '\n    Container for a consul service record\n    Example:\n\n        # Consul advertises a service called FOO that is reachable via two URIs:\n        # http://10.1.1.1:8001 and http://10.1.1.2:8002\n    cs = ConsulService("consul://tag.FOO.service")\n\n        # Set the DNS nameserver to the default docker0 bridge ip\n    cs = ConsulService("consul://tag.FOO.server", nameservers=[\'172.17.42.1\'])\n\n        # returns a random choice from the DNS-advertised routes\n        # in our case, either http://10.1.1.1:8001 or http://10.1.1.2:8002\n    cs.base_url\n\n        # send an http-get to base_url+\'/v1/status\', re-resolving and\n        # re-retrying if that connection failed\n    cs.get(\'/v1/status\')\n\n        #Subsequent http requests will now have the "X-Added" header\n    cs.session.headers.update({"X-Added": "Value"})\n    cs.post(\'/v1/status\')\n    '

    def __init__(self, service_uri, nameservers=None):
        """
        :param service_uri: string formatted service identifier
            (consul://production.solr_service.consul)
        :param nameservers: use custom nameservers
        :type nameservers: list
        """
        assert service_uri.startswith('consul://'), 'Invalid consul service URI'
        self.service_uri = service_uri
        self.service = service_uri.replace('consul://', '')
        self.resolver = Resolver()
        self.session = requests.Session()
        if nameservers is not None:
            self.resolver.nameservers = nameservers

    def _resolve(self):
        """
        Query the consul DNS server for the service IP and port
        """
        endpoints = {}
        r = self.resolver.query(self.service, 'SRV')
        for rec in r.response.additional:
            name = rec.name.to_text()
            addr = rec.items[0].address
            endpoints[name] = {'addr': addr}

        for rec in r.response.answer[0].items:
            name = '.'.join(rec.target.labels)
            endpoints[name]['port'] = rec.port

        return ['http://{ip}:{port}'.format(ip=v['addr'], port=v['port']) for v in endpoints.values()]

    @property
    def base_url(self):
        """
        get the next endpoint from self.endpoints
        """
        return self._resolve().pop()

    @with_retry_connections()
    def request(self, method, endpoint, **kwargs):
        """
        Proxy to requests.request
        :param method: str formatted http method
        :param endpoint: service endpoint
        :param kwargs: kwargs passed directly to requests.request
        :return:
        """
        kwargs.setdefault('timeout', (1, 30))
        return self.session.request(method, urljoin(self.base_url, endpoint), **kwargs)

    def get(self, endpoint, **kwargs):
        return self.request('GET', endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self.request('POST', endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self.request('DELETE', endpoint, **kwargs)

    def put(self, endpoint, **kwargs):
        return self.request('PUT', endpoint, **kwargs)

    def options(self, endpoint, **kwargs):
        return self.request('OPTIONS', endpoint, **kwargs)

    def head(self, endpoint, **kwargs):
        return self.request('HEAD', endpoint, **kwargs)