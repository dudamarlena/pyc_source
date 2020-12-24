# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/js/dev/prl/dart/pybind11/python/tests/unit/common/test_uri.py
# Compiled at: 2018-10-11 07:21:58
# Size of source mod 2**32: 827 bytes
import unittest
from dartpy.common import Uri

class TestUri(unittest.TestCase):

    def test_from_string_valid_uri_returns_true(self):
        uri = Uri()
        self.assertTrue(uri.fromString('ftp://ftp.is.co.za/rfc/rfc1808.txt'))
        self.assertTrue(uri.fromString('http://www.ietf.org/rfc/rfc2396.txt'))
        self.assertTrue(uri.fromString('ldap://[2001:db8::7]/c=GB?objectClass?one'))
        self.assertTrue(uri.fromString('mailto:John.Doe@example.com'))
        self.assertTrue(uri.fromString('news:comp.infosystems.www.servers.unix'))
        self.assertTrue(uri.fromString('tel:+1-816-555-1212'))
        self.assertTrue(uri.fromString('telnet://192.0.2.16:80/'))
        self.assertTrue(uri.fromString('urn:oasis:names:specification:docbook:dtd:xml:4.1.2'))


if __name__ == '__main__':
    unittest.main()