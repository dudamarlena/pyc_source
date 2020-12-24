# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit_vpp/tests/protocols/test_base_classes.py
# Compiled at: 2017-06-08 14:18:32
# Size of source mod 2**32: 760 bytes
import unittest
from dhcpkit_vpp.protocols import Layer4Protocol, Layer3Packet
from dhcpkit_vpp.protocols.layer4 import UnknownLayer4Protocol

class Layer3PacketTestCase(unittest.TestCase):

    def test_abstract_get_pseudo_header(self):
        obj = Layer3Packet()
        l4_obj = UnknownLayer4Protocol()
        with self.assertRaises(NotImplementedError):
            obj.get_pseudo_header(l4_obj)


class Layer4ProtocolTestCase(unittest.TestCase):

    def test_abstract_length(self):
        obj = Layer4Protocol()
        with self.assertRaises(NotImplementedError):
            self.assertIsNone(obj.length)

    def test_abstract_save(self):
        obj = Layer4Protocol()
        with self.assertRaises(NotImplementedError):
            obj.save()