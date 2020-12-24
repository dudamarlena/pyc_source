# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/ipv6/test_duids.py
# Compiled at: 2017-06-24 07:07:07
# Size of source mod 2**32: 7982 bytes
"""
Test the included DUID types
"""
import unittest
from dhcpkit.ipv6.duids import DUID, EnterpriseDUID, LinkLayerDUID, LinkLayerTimeDUID, UnknownDUID

class UnknownDUIDTestCase(unittest.TestCase):

    def setUp(self):
        self.duid_object = UnknownDUID(duid_type=65535, duid_data=b'SomeRandomDUIDData')
        self.duid_bytes = bytes.fromhex('ffff536f6d6552616e646f6d4455494444617461')

    def test_hash(self):
        duid_hash = hash(self.duid_object)
        self.assertIsInstance(duid_hash, int)

    def test_parse(self):
        with self.assertRaisesRegex(ValueError, 'length'):
            DUID.parse(self.duid_bytes)
        length = len(self.duid_bytes)
        parsed_length, parsed_object = DUID.parse(self.duid_bytes, length=length)
        self.assertEqual(parsed_length, length)
        self.assertEqual(parsed_object, self.duid_object)

    def test_parse_with_larger_buffer(self):
        offset = 50
        buffer = bytes(50 * [0]) + self.duid_bytes + bytes(50 * [0])
        length = len(self.duid_bytes)
        parsed_length, parsed_object = DUID.parse(buffer, offset=offset, length=length)
        self.assertEqual(parsed_length, length)
        self.assertEqual(parsed_object, self.duid_object)

    def test_save(self):
        saved_bytes = self.duid_object.save()
        self.assertEqual(saved_bytes, self.duid_bytes)


class LinkLayerTimeDUIDTestCase(UnknownDUIDTestCase):

    def setUp(self):
        self.duid_object = LinkLayerTimeDUID(hardware_type=1, time=15, link_layer_address=bytes.fromhex('3431c43cb2f1'))
        self.duid_bytes = bytes.fromhex('000100010000000f3431c43cb2f1')

    def test_wrong_parser(self):
        with self.assertRaisesRegex(ValueError, 'does not contain LinkLayerDUID'):
            duid = LinkLayerDUID()
            duid.load_from(self.duid_bytes, length=len(self.duid_bytes))

    def test_validate_hardware_type(self):
        good_duid_object = LinkLayerTimeDUID(0, 0, b'demo')
        good_duid_object.validate()
        bad_duid_object = LinkLayerTimeDUID(-1, 0, b'demo')
        with self.assertRaisesRegex(ValueError, 'unsigned 16 bit integer'):
            bad_duid_object.validate()
        bad_duid_object = LinkLayerTimeDUID(65536, 0, b'demo')
        with self.assertRaisesRegex(ValueError, 'unsigned 16 bit integer'):
            bad_duid_object.validate()

    def test_validate_time(self):
        good_duid_object = LinkLayerTimeDUID(0, 0, b'demo')
        good_duid_object.validate()
        bad_duid_object = LinkLayerTimeDUID(0, -1, b'demo')
        with self.assertRaisesRegex(ValueError, 'unsigned 32 bit integer'):
            bad_duid_object.validate()
        bad_duid_object = LinkLayerTimeDUID(0, 4294967296, b'demo')
        with self.assertRaisesRegex(ValueError, 'unsigned 32 bit integer'):
            bad_duid_object.validate()

    def test_validate_link_layer(self):
        bad_duid_object = LinkLayerTimeDUID(0, 0, 'demo')
        with self.assertRaisesRegex(ValueError, 'sequence of bytes'):
            bad_duid_object.validate()

    def test_validate_length(self):
        good_duid_object = LinkLayerTimeDUID(0, 0, 120 * b'x')
        good_duid_object.validate()
        bad_duid_object = LinkLayerTimeDUID(0, 0, 121 * b'x')
        with self.assertRaisesRegex(ValueError, 'cannot be longer than 120 bytes'):
            bad_duid_object.validate()

    def test_display_ethernet(self):
        output = str(self.duid_object)
        self.assertEqual(output, 'LinkLayerTimeDUID(\n  hardware_type=Ethernet (1),\n  time=15,\n  link_layer_address=34:31:c4:3c:b2:f1,\n)')

    def test_display_other(self):
        self.duid_object.hardware_type = 2
        output = str(self.duid_object)
        self.assertEqual(output, "LinkLayerTimeDUID(\n  hardware_type=Experimental Ethernet (2),\n  time=15,\n  link_layer_address=b'41\\xc4<\\xb2\\xf1',\n)")


class EnterpriseDUIDTestCase(UnknownDUIDTestCase):

    def setUp(self):
        self.duid_object = EnterpriseDUID(enterprise_number=40208, identifier=b'DHCPKitUnitTestIdentifier')
        self.duid_bytes = bytes.fromhex('000200009d10444843504b6974556e6974546573744964656e746966696572')

    def test_wrong_parser(self):
        with self.assertRaisesRegex(ValueError, 'does not contain LinkLayerTimeDUID'):
            duid = LinkLayerTimeDUID()
            duid.load_from(self.duid_bytes, length=len(self.duid_bytes))

    def test_validate_enterprise_number(self):
        good_duid_object = EnterpriseDUID(0, b'demo')
        good_duid_object.validate()
        bad_duid_object = EnterpriseDUID(-1, b'demo')
        with self.assertRaisesRegex(ValueError, 'unsigned 32 bit integer'):
            bad_duid_object.validate()
        bad_duid_object = EnterpriseDUID(4294967296, b'demo')
        with self.assertRaisesRegex(ValueError, 'unsigned 32 bit integer'):
            bad_duid_object.validate()

    def test_validate_identifier(self):
        bad_duid_object = EnterpriseDUID(0, 'demo')
        with self.assertRaisesRegex(ValueError, 'sequence of bytes'):
            bad_duid_object.validate()

    def test_validate_length(self):
        good_duid_object = EnterpriseDUID(0, 122 * b'x')
        good_duid_object.validate()
        bad_duid_object = EnterpriseDUID(0, 123 * b'x')
        with self.assertRaisesRegex(ValueError, 'cannot be longer than 122 bytes'):
            bad_duid_object.validate()


class LinkLayerDUIDTestCase(UnknownDUIDTestCase):

    def setUp(self):
        self.duid_object = LinkLayerDUID(hardware_type=1, link_layer_address=bytes.fromhex('3431c43cb2f1'))
        self.duid_bytes = bytes.fromhex('000300013431c43cb2f1')

    def test_wrong_parser(self):
        with self.assertRaisesRegex(ValueError, 'does not contain EnterpriseDUID'):
            duid = EnterpriseDUID()
            duid.load_from(self.duid_bytes, length=len(self.duid_bytes))

    def test_validate_hardware_type(self):
        good_duid_object = LinkLayerDUID(0, b'demo')
        good_duid_object.validate()
        bad_duid_object = LinkLayerDUID(-1, b'demo')
        with self.assertRaisesRegex(ValueError, 'unsigned 16 bit integer'):
            bad_duid_object.validate()
        bad_duid_object = LinkLayerDUID(65536, b'demo')
        with self.assertRaisesRegex(ValueError, 'unsigned 16 bit integer'):
            bad_duid_object.validate()

    def test_validate_link_layer(self):
        bad_duid_object = LinkLayerDUID(0, 'demo')
        with self.assertRaisesRegex(ValueError, 'sequence of bytes'):
            bad_duid_object.validate()

    def test_validate_length(self):
        good_duid_object = LinkLayerDUID(0, 124 * b'x')
        good_duid_object.validate()
        bad_duid_object = LinkLayerDUID(0, 125 * b'x')
        with self.assertRaisesRegex(ValueError, 'cannot be longer than 124 bytes'):
            bad_duid_object.validate()

    def test_display_ethernet(self):
        output = str(self.duid_object)
        self.assertEqual(output, 'LinkLayerDUID(\n  hardware_type=Ethernet (1),\n  link_layer_address=34:31:c4:3c:b2:f1,\n)')

    def test_display_other(self):
        self.duid_object.hardware_type = 2
        output = str(self.duid_object)
        self.assertEqual(output, "LinkLayerDUID(\n  hardware_type=Experimental Ethernet (2),\n  link_layer_address=b'41\\xc4<\\xb2\\xf1',\n)")


if __name__ == '__main__':
    unittest.main()