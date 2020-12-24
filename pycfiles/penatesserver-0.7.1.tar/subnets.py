# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mgallet/Github/Penates-Server/penatesserver/subnets.py
# Compiled at: 2015-10-19 03:33:47
from __future__ import unicode_literals
from django.utils.lru_cache import lru_cache
from django.conf import settings
from netaddr import IPNetwork, IPAddress
__author__ = b'Matthieu Gallet'

class Subnet(object):

    def __init__(self, network, router):
        assert isinstance(network, IPNetwork)
        assert isinstance(router, IPAddress)
        self.network = network
        self.router = router

    @property
    def mask(self):
        return str(self.network.netmask)

    @property
    def address(self):
        return str(self.network.network)

    @property
    def mask_len(self):
        return self.network.prefixlen

    @property
    def broadcast(self):
        return str(self.network.broadcast)

    @property
    def start(self):
        size = 32 if self.network.version == 4 else 128
        return str(self.network.network + 2 ** max(size - self.network.prefixlen - 3, 0))

    @property
    def end(self):
        size = 32 if self.network.version == 4 else 128
        return str(self.network.network - 2 + 2 ** (size - self.network.prefixlen))


@lru_cache()
def get_subnets():
    all_subnets = []
    done = set()
    for line in settings.PENATES_SUBNETS.splitlines():
        line = line.strip()
        if not line:
            continue
        network_str, sep, router_str = line.partition(b',')
        if sep != b',':
            raise ValueError(b'Invalid PENATES_SUBNETS: %s' % line)
        if network_str in done:
            continue
        done.add(network_str)
        network = IPNetwork(network_str)
        router = IPAddress(router_str)
        all_subnets.append(Subnet(network, router))

    return all_subnets