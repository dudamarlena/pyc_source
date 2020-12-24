# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/errr/programs/python/thunderhead/tests/connection_tests.py
# Compiled at: 2014-09-15 00:03:48
import tests
from thunderhead.connection import Connection
from thunderhead.exceptions import MissingProperty

class ConnectionTests(tests.ThunderheadTests):

    def test_build_url_throws_missing_property(self):
        connection = Connection(port=8443, protocol='https')
        self.assertRaises(MissingProperty, connection.build_url)

    def test_build_url_strips_ending_slashes_from_command(self):
        host = 'localhost'
        port = 8443
        command = 'customers/'
        connection = Connection(host=host, port=port, command=command)
        path = connection.base_path
        proto = connection.protocol
        url = ('{0}://{1}:{2}/{3}/customers').format(proto, host, port, path)
        self.assertEqual(url, connection.build_url())