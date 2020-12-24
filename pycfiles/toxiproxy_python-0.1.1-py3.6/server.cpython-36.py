# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/toxiproxy/server.py
# Compiled at: 2018-09-04 11:50:42
# Size of source mod 2**32: 3325 bytes
from future.utils import raise_with_traceback, viewitems, listvalues
from .api import APIConsumer
from .proxy import Proxy
from .exceptions import ProxyExists
from .utils import can_connect_to

class Toxiproxy(object):
    __doc__ = ' Represents a Toxiproxy server '

    def proxies(self):
        """ Returns all the proxies registered in the server """
        proxies = APIConsumer.get('/proxies').json()
        proxies_dict = {}
        for name, values in viewitems(proxies):
            proxy = Proxy(**values)
            proxies_dict.update({name: proxy})

        return proxies_dict

    def destroy_all(self):
        proxies = listvalues(self.proxies())
        for proxy in proxies:
            self.destroy(proxy)

    def get_proxy(self, proxy_name):
        """ Retrive a proxy if it exists """
        proxies = self.proxies()
        if proxy_name in proxies:
            return proxies[proxy_name]
        else:
            return

    def running(self):
        """ Test if the toxiproxy server is running """
        return can_connect_to(APIConsumer.host, APIConsumer.port)

    def version(self):
        """ Get the toxiproxy server version """
        if self.running() is True:
            return APIConsumer.get('/version').content
        else:
            return

    def reset(self):
        """ Re-enables all proxies and disables all toxics. """
        return bool(APIConsumer.post('/reset'))

    def create(self, upstream, name, listen=None, enabled=None):
        """ Create a toxiproxy proxy """
        if name in self.proxies():
            raise_with_traceback(ProxyExists('This proxy already exists.'))
        else:
            json = {'upstream':upstream,  'name':name}
            if listen is not None:
                json['listen'] = listen
            else:
                json['listen'] = '127.0.0.1:0'
        if enabled is not None:
            json['enabled'] = enabled
        proxy_info = APIConsumer.post('/proxies', json=json).json()
        proxy_info['api_consumer'] = APIConsumer
        proxy = Proxy(**proxy_info)
        return proxy

    def destroy(self, proxy):
        """ Delete a toxiproxy proxy """
        if isinstance(proxy, Proxy):
            return proxy.destroy()
        else:
            return False

    def populate(self, proxies):
        """ Create a list of proxies from an array """
        populated_proxies = []
        for proxy in proxies:
            existing = self.get_proxy(proxy['name'])
            if existing is not None:
                if existing.upstream != proxy['upstream'] or existing.listen != proxy['listen']:
                    self.destroy(existing)
                    existing = None
                if existing is None:
                    proxy_instance = (self.create)(**proxy)
                    populated_proxies.append(proxy_instance)

        return populated_proxies

    def update_api_consumer(self, host, port):
        """ Update the APIConsumer host and port """
        APIConsumer.host = host
        APIConsumer.port = port