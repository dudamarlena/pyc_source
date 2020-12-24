# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ldpy/client.py
# Compiled at: 2015-11-04 02:45:20
import requests
from rdflib.graph import Graph
_rdflibFormatsMappings = {'text/turtle': 'turtle', 
   'application/rdf+xml': 'xml', 
   'text/n3': 'n3', 
   'application/n-triples': 'nt', 
   'application/trix': 'trix'}

def _getUserAgent():
    try:
        import ldpy
        return ldpy.__agent__
    except ImportError:
        return 'ldpy'


class Client:

    def __init__(self, server, userAgent=_getUserAgent()):
        self.server = server
        self.userAgent = userAgent
        try:
            requests.head(self.server)
        except requests.exceptions.ConnectionError as e:
            raise ValueError('server %s does not look to be alive: %s' % (server, e.message))

    def create(self, container=None, payload=None, format=None, tentativeName=None):
        if container is None:
            container = self.server
        elif not container.startswith(self.server):
            raise ValueError('base container %s does not belong to this client instance', container)
        if payload:
            if type(payload) == str:
                pass
            elif type(payload) == file:
                payload = payload.read()
            elif type(payload) == Graph:
                format = _rdflibFormatsMappings[format] if format in _rdflibFormatsMappings else 'turtle'
                payload = payload.serialize(format=format)
            else:
                raise ValueError('unsupported type %s as payload' % type(payload))
        headers = {'Content-Type': 'text/turtle', 'User-Agent': self.userAgent}
        if tentativeName is not None and len(tentativeName) > 0:
            headers['Slug'] = tentativeName
        request = requests.post(container, data=payload, headers=headers)
        if request.status_code == 201:
            return request.headers['Location']
        else:
            raise RuntimeError('creation of resource in container %s failed, server returned %d status code' % (container, request.status_code))
            return

    def read(self, resource, format=None):
        if not resource.startswith(self.server):
            raise ValueError('requested resource %s does not belong to this client instance' % resource)
        if format not in _rdflibFormatsMappings:
            format = 'text/turtle'
        request = requests.get(resource, headers={'Accept': format, 'User-Agent': self.userAgent})
        if request.status_code != 200:
            raise RuntimeError('reading resource %s failed, server returned %d status code' % (resource, request.status_code))
        else:
            if request.headers['Content-Type'] in _rdflibFormatsMappings:
                g = Graph()
                g.parse(data=request.text, format=_rdflibFormatsMappings[request.headers['Content-Type']])
                return g
            else:
                return request.text