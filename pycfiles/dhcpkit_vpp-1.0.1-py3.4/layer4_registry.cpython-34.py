# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit_vpp/protocols/layer4_registry.py
# Compiled at: 2017-06-07 13:58:11
# Size of source mod 2**32: 300 bytes
"""
The protocol layer 4 registry
"""
from dhcpkit.registry import Registry

class ProtocolLayer4Registry(Registry):
    __doc__ = '\n    Registry for Protocols\n    '
    entry_point = 'dhcpkit_vpp.protocols.layer4'


protocol_layer4_registry = ProtocolLayer4Registry()