# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/martijndevos/Documents/anydex-core/anydex/../pyipv8/ipv8/messaging/anonymization/pex.py
# Compiled at: 2019-05-16 09:27:10
from __future__ import absolute_import
import random, time
from collections import deque
from ...community import Community
from ...messaging.anonymization.tunnel import IntroductionPoint, PEER_SOURCE_PEX
from ...messaging.deprecated.encoding import decode, encode
from ...messaging.interfaces.endpoint import Endpoint, EndpointListener
from ...peer import Peer

class PexEndpointAdapter(Endpoint, EndpointListener):

    def __init__(self, master):
        Endpoint.__init__(self)
        EndpointListener.__init__(self, master)
        self.master = master
        self.master.add_listener(self)
        self._listeners = {}
        self._port = 0

    def add_listener(self, listener):
        self._listeners[listener.get_prefix()] = listener

    def remove_listener(self, listener):
        self._listeners.pop(listener.get_prefix(), None)
        return

    def on_packet(self, packet):
        listener = self._listeners.get(packet[1][:22], None)
        if listener:
            listener.on_packet(packet)
        return

    def assert_open(self):
        self.master.assert_open()

    def is_open(self):
        return self.master.is_open()

    def get_address(self):
        return self.master.get_address()

    def send(self, socket_address, packet):
        self.master.send(socket_address, packet)

    def open(self):
        out = self.master.open()
        self._port = self.master._port
        return out

    def close(self):
        return self.master.close()


class PexMasterPeer(object):

    def __init__(self, info_hash):
        self.mid = info_hash


class PexCommunity(Community):

    def __init__(self, *args, **kwargs):
        self.master_peer = PexMasterPeer(kwargs.pop('info_hash'))
        self._prefix = '\x00' + self.version + self.master_peer.mid
        super(PexCommunity, self).__init__(*args, **kwargs)
        self.intro_points = deque(maxlen=20)
        self.intro_points_for = []

    def get_intro_points(self):
        """
        Get a list of the most recent introduction points that were discovered using PexCommunity.
        :return : list of IntroductionPoint objects
        """
        now = time.time()
        while self.intro_points and self.intro_points[(-1)].last_seen + 300 < now:
            self.intro_points.pop()

        my_peer = Peer(self.my_peer.key, self.my_estimated_wan)
        return list(self.intro_points) + [ IntroductionPoint(my_peer, seeder_pk, PEER_SOURCE_PEX) for seeder_pk in self.intro_points_for
                                         ]

    def start_announce(self, seeder_pk):
        """
        Start announcing yourself as an introduction point for a certain seeder.
        :param seeder_pk: public key of the seeder (in binary format)
        """
        if seeder_pk not in self.intro_points_for:
            self.intro_points_for.append(seeder_pk)

    def stop_announce(self, seeder_pk):
        """
        Stop announcing yourself as an introduction point for a certain seeder.
        :param seeder_pk: public key of the seeder (in binary format)
        """
        if seeder_pk in self.intro_points_for:
            self.intro_points_for.remove(seeder_pk)

    @property
    def done(self):
        return not bool(self.intro_points_for)

    def process_extra_bytes(self, peer, extra_bytes):
        if not extra_bytes:
            return
        for seeder_pk in decode(extra_bytes)[1]:
            ip = IntroductionPoint(peer, seeder_pk, PEER_SOURCE_PEX)
            if ip in self.intro_points:
                self.intro_points.remove(ip)
            self.intro_points.appendleft(ip)

    def introduction_request_callback(self, peer, dist, payload):
        self.process_extra_bytes(peer, payload.extra_bytes)

    def introduction_response_callback(self, peer, dist, payload):
        self.process_extra_bytes(peer, payload.extra_bytes)

    def create_introduction_request(self, socket_address, extra_bytes=''):
        extra_bytes = encode(random.sample(self.intro_points_for, min(len(self.intro_points_for), 10)))
        return super(PexCommunity, self).create_introduction_request(socket_address, extra_bytes)

    def create_introduction_response(self, lan_socket_address, socket_address, identifier, introduction=None, extra_bytes=''):
        extra_bytes = encode(random.sample(self.intro_points_for, min(len(self.intro_points_for), 10)))
        return super(PexCommunity, self).create_introduction_response(lan_socket_address, socket_address, identifier, introduction, extra_bytes)