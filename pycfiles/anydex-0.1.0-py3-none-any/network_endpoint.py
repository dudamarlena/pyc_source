# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/martijndevos/Documents/anydex-core/pyipv8/ipv8/REST/network_endpoint.py
# Compiled at: 2019-05-22 05:00:30
from __future__ import absolute_import
from base64 import b64encode
from .base_endpoint import BaseEndpoint

class NetworkEndpoint(BaseEndpoint):
    """
    This endpoint is responsible for handing all requests regarding the state of the network.
    """

    def __init__(self, session):
        super(NetworkEndpoint, self).__init__()
        self.session = session

    def retrieve_peers(self):
        network = self.session.network
        peer_list = network.verified_peers[:]
        return {b64encode(peer.mid):{'ip': peer.address[0], 'port': peer.address[1], 'public_key': b64encode(peer.public_key.key_to_bin()), 'services': [ b64encode(s) for s in network.get_services_for_peer(peer) ]} for peer in peer_list}

    def render_GET(self, request):
        return self.twisted_dumps({'peers': self.retrieve_peers()})