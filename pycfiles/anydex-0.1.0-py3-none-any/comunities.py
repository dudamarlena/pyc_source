# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/martijndevos/Documents/anydex-core/pyipv8/ipv8/test/mocking/rest/comunities.py
# Compiled at: 2019-05-16 09:27:10
from __future__ import absolute_import
from ....attestation.identity.community import IdentityCommunity
from ....attestation.wallet.community import AttestationCommunity
from ....attestation.trustchain.community import TrustChainCommunity
from ....dht.community import DHTCommunity
from ....keyvault.crypto import ECCrypto
from ....peer import Peer

class TestAttestationCommunity(AttestationCommunity):
    master_peer = Peer(ECCrypto().generate_key('high'))


class TestIdentityCommunity(IdentityCommunity):
    master_peer = Peer(ECCrypto().generate_key('high'))


class TestDHTCommunity(DHTCommunity):
    master_peer = Peer(ECCrypto().generate_key('high'))


class TestTrustchainCommunity(TrustChainCommunity):
    master_peer = Peer(ECCrypto().generate_key('high'))


def overlay_initializer(overlay_class, my_peer, endpoint, network, working_directory):
    """
    Wrapper class, which instantiates new overlay classes.

    :param overlay_class: the overlay's class
    :param my_peer: the peer passed to the overlay
    :param endpoint: the endpoint passed to the overlay
    :param network:  the network passer to the overlay
    :param working_directory: the overlay's working directory
    :return: an initialized object of the overlay_class type
    """
    if issubclass(overlay_class, DHTCommunity):
        return overlay_class(my_peer, endpoint, network)
    return overlay_class(my_peer, endpoint, network, working_directory=working_directory)