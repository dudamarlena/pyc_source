# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/martijndevos/Documents/anydex-core/anydex/../pyipv8/ipv8/REST/root_endpoint.py
# Compiled at: 2019-06-07 08:10:38
from __future__ import absolute_import
from .attestation_endpoint import AttestationEndpoint
from .base_endpoint import BaseEndpoint
from .dht_endpoint import DHTEndpoint
from .isolation_endpoint import IsolationEndpoint
from .network_endpoint import NetworkEndpoint
from .noblock_dht_endpoint import NoBlockDHTEndpoint
from .overlays_endpoint import OverlaysEndpoint
from .trustchain_endpoint import TrustchainEndpoint
from .tunnel_endpoint import TunnelEndpoint

class RootEndpoint(BaseEndpoint):
    """
    The root endpoint of the HTTP API is the root resource in the request tree.
    It will dispatch requests regarding torrents, channels, settings etc to the right child endpoint.
    """

    def __init__(self, session):
        """
        During the initialization of the REST API, we only start the event sockets and the state endpoint.
        We enable the other endpoints after completing the starting procedure.
        """
        super(RootEndpoint, self).__init__()
        self.session = session
        self.putChild('attestation', AttestationEndpoint(session))
        self.putChild('dht', DHTEndpoint(session))
        self.putChild('isolation', IsolationEndpoint(session))
        self.putChild('network', NetworkEndpoint(session))
        self.putChild('noblockdht', NoBlockDHTEndpoint(session))
        self.putChild('overlays', OverlaysEndpoint(session))
        self.putChild('trustchain', TrustchainEndpoint(session))
        self.putChild('tunnel', TunnelEndpoint(session))