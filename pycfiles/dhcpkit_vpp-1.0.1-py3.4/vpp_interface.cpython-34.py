# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit_vpp/listeners/vpp/vpp_interface.py
# Compiled at: 2017-06-20 18:30:31
# Size of source mod 2**32: 1446 bytes
from ipaddress import IPv6Address
from dhcpkit.ipv6 import All_DHCP_Relay_Agents_and_Servers
from dhcpkit.ipv6.server.listeners import ListeningSocketError
from dhcpkit_vpp.vpp_papi import VPP

class VPPInterface:
    __doc__ = '\n    A simple container to keep information about VPP interfaces in\n    '

    def __init__(self, vpp: VPP, name: str, index: int, mac_address: bytes, accept_unicast: bool, accept_multicast: bool, reply_from: IPv6Address, link_address: IPv6Address):
        self.vpp = vpp
        self.name = name
        self.index = index
        self.mac_address = mac_address
        self.accept_unicast = accept_unicast
        self.accept_multicast = accept_multicast
        self.reply_from = reply_from
        self.link_address = link_address

    def activate(self):
        """
        Activate this interface and make VPP listen to multicast if necessary
        """
        if self.accept_multicast:
            rv = self.vpp.api.ip_mroute_add_del(next_hop_sw_if_index=self.index, grp_address_length=128, is_add=1, is_ipv6=1, itf_flags=2, grp_address=All_DHCP_Relay_Agents_and_Servers.packed)
            if rv.retval != 0:
                raise ListeningSocketError("Can't make interface {} listen to the multicast address".format(self.index))