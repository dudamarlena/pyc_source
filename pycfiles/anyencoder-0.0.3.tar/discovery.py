# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: pyipv8/ipv8/test/mocking/discovery.py
# Compiled at: 2019-05-16 09:27:10
from __future__ import absolute_import
from ...peerdiscovery.discovery import DiscoveryStrategy

class MockWalk(DiscoveryStrategy):

    def take_step(self):
        for peer in self.overlay.network.verified_peers:
            self.overlay.walk_to(peer.address)