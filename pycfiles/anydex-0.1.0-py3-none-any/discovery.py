# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pyipv8/ipv8/test/mocking/discovery.py
# Compiled at: 2019-05-16 09:27:10
from __future__ import absolute_import
from ...peerdiscovery.discovery import DiscoveryStrategy

class MockWalk(DiscoveryStrategy):

    def take_step(self):
        for peer in self.overlay.network.verified_peers:
            self.overlay.walk_to(peer.address)