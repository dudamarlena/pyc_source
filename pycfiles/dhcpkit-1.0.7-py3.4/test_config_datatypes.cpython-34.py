# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/dhcpkit/tests/common/server/test_config_datatypes.py
# Compiled at: 2017-06-23 17:22:45
# Size of source mod 2**32: 3190 bytes
"""
Tests for datatypes for use in configuration files
"""
import unittest
from dhcpkit.common.server.config_datatypes import domain_name

class DomainNameTestCase(unittest.TestCase):

    def test_valid(self):
        valid_domain_names = [
         ('steffann.nl', 'steffann.nl'),
         ('steffann.nl.', 'steffann.nl.'),
         ('Steffann.Nl', 'steffann.nl'),
         ('Steffann.Nl.', 'steffann.nl.'),
         ('STEFFANN.NL', 'steffann.nl'),
         ('STEFFANN.NL.', 'steffann.nl.'),
         ('10ww.steffann.nl', '10ww.steffann.nl'),
         ('local', 'local'),
         ('LOCAL', 'local'),
         ('10ww.steffann-steffann-steffann-steffann-steffann-steffann-steffann.steffann-steffann-steffann-steffann-steffann-steffann-steffann.steffann-steffann-steffann-steffann-steffann-steffann-steffann.steffann-steffann-steffann-steffann-steffann-steffann-st.nl',
 '10ww.steffann-steffann-steffann-steffann-steffann-steffann-steffann.steffann-steffann-steffann-steffann-steffann-steffann-steffann.steffann-steffann-steffann-steffann-steffann-steffann-steffann.steffann-steffann-steffann-steffann-steffann-steffann-st.nl'),
         ('10ww.steffann-steffann-steffann-steffann-steffann-steffann-steffann.steffann-steffann-steffann-steffann-steffann-steffann-steffann.steffann-steffann-steffann-steffann-steffann-steffann-steffann.steffann-steffann-steffann-steffann-steffann-steffann-st.nl.',
 '10ww.steffann-steffann-steffann-steffann-steffann-steffann-steffann.steffann-steffann-steffann-steffann-steffann-steffann-steffann.steffann-steffann-steffann-steffann-steffann-steffann-steffann.steffann-steffann-steffann-steffann-steffann-steffann-st.nl.')]
        for test, output in valid_domain_names:
            with self.subTest(test=test):
                self.assertEqual(domain_name(test), output)

    def test_name_too_long(self):
        oversized_domain_name = '10ww.steffann-steffann-steffann-steffann-steffann-steffann-steffann.steffann-steffann-steffann-steffann-steffann-steffann-steffann.steffann-steffann-steffann-steffann-steffann-steffann-steffann.steffann-steffann-steffann-steffann-steffann-steffann-ste.nl'
        with self.assertRaisesRegex(ValueError, 'Domain too long'):
            domain_name(oversized_domain_name)

    def test_label_too_long(self):
        oversized_label_name = '10ww.steffann-steffann-steffann-steffann-steffann-steffann-steffann-steffann.nl'
        with self.assertRaisesRegex(ValueError, 'Label too long'):
            domain_name(oversized_label_name)


if __name__ == '__main__':
    unittest.main()