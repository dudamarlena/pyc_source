# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/martijndevos/Documents/anydex-core/pyipv8/ipv8/test/mocking/rest/ipv8.py
# Compiled at: 2019-05-16 09:27:10
from __future__ import absolute_import
import threading
from twisted.internet.task import LoopingCall
from .comunities import TestIdentityCommunity, TestAttestationCommunity, overlay_initializer
from ....keyvault.crypto import ECCrypto
from ....messaging.interfaces.udp.endpoint import UDPEndpoint
from ....peer import Peer
from ....peerdiscovery.discovery import RandomWalk
from ....peerdiscovery.network import Network

class TestRestIPv8(object):

    def __init__(self, crypto_curve, port, interface, overlay_classes, memory_dbs=True):
        self.memory_dbs = memory_dbs
        self.endpoint = UDPEndpoint(port=port, ip=interface)
        self.endpoint.open()
        self.network = Network()
        my_peer = Peer(ECCrypto().generate_key(crypto_curve))
        self.keys = {'my_peer': my_peer}
        database_working_dir = ':memory:' if memory_dbs else ''
        self.overlays = []
        for overlay_class in overlay_classes:
            self.overlays.append(overlay_initializer(overlay_class, my_peer, self.endpoint, self.network, working_directory=database_working_dir))

        self.strategies = [ (RandomWalk(overlay), 20) for overlay in self.overlays ]
        self.overlay_lock = threading.RLock()
        self.state_machine_lc = LoopingCall(self.on_tick)
        self.state_machine_lc.start(0.5, False)

    def on_tick(self):
        if self.endpoint.is_open():
            with self.overlay_lock:
                for strategy, target_peers in self.strategies:
                    peer_count = len(strategy.overlay.get_peers())
                    if target_peers == -1 or peer_count < target_peers:
                        strategy.take_step()

    def unload(self):
        if self.state_machine_lc.running:
            self.state_machine_lc.stop()
        if self.endpoint.is_open():
            self.endpoint.close()
        for overlay in self.overlays:
            if isinstance(overlay, TestAttestationCommunity):
                overlay.database.close()
            elif isinstance(overlay, TestIdentityCommunity):
                overlay.persistence.close()
            overlay.request_cache.clear()
            overlay.unload()