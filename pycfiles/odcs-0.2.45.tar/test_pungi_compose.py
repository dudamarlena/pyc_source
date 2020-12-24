# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hanzz/releases/odcs/server/tests/test_pungi_compose.py
# Compiled at: 2019-01-28 02:13:22
import six, unittest
from mock import patch
from odcs.server.pungi_compose import PungiCompose
RPMS_JSON = {'header': {'type': 'productmd.rpms', 
              'version': '1.2'}, 
   'payload': {'compose': {'date': '20181210', 
                           'id': 'odcs-691-1-20181210.n.0', 
                           'respin': 0, 
                           'type': 'nightly'}, 
               'rpms': {'Temporary': {'x86_64': {'flatpak-rpm-macros-0:29-6.module+125+c4f5c7f2.src': {'flatpak-rpm-macros-0:29-6.module+125+c4f5c7f2.src': {'category': 'source', 
                                                                                                                                                             'path': 'Temporary/source/tree/Packages/f/flatpak-rpm-macros-29-6.module+125+c4f5c7f2.src.rpm', 
                                                                                                                                                             'sigkey': None}, 
                                                                                                       'flatpak-rpm-macros-0:29-6.module+125+c4f5c7f2.x86_64': {'category': 'binary', 
                                                                                                                                                                'path': 'Temporary/x86_64/os/Packages/f/flatpak-rpm-macros-29-6.module+125+c4f5c7f2.x86_64.rpm', 
                                                                                                                                                                'sigkey': None}}, 
                                                 'flatpak-runtime-config-0:29-4.module+125+c4f5c7f2.src': {'flatpak-runtime-config-0:29-4.module+125+c4f5c7f2.src': {'category': 'source', 
                                                                                                                                                                     'path': 'Temporary/source/tree/Packages/f/flatpak-runtime-config-29-4.module+125+c4f5c7f2.src.rpm', 
                                                                                                                                                                     'sigkey': 'sigkey1'}, 
                                                                                                           'flatpak-runtime-config-0:29-4.module+125+c4f5c7f2.x86_64': {'category': 'binary', 
                                                                                                                                                                        'path': 'Temporary/x86_64/os/Packages/f/flatpak-runtime-config-29-4.module+125+c4f5c7f2.x86_64.rpm', 
                                                                                                                                                                        'sigkey': 'sigkey1'}}}}}}}

@patch('odcs.server.pungi_compose.PungiCompose._fetch_json')
class TestPungiCompose(unittest.TestCase):

    def test_get_rpms_data(self, fetch_json):
        fetch_json.return_value = RPMS_JSON
        compose = PungiCompose('http://localhost/compose/Temporary')
        data = compose.get_rpms_data()
        expected = {'sigkeys': set(['sigkey1', None]), 
           'arches': set(['x86_64']), 
           'builds': {'flatpak-rpm-macros-29-6.module+125+c4f5c7f2': set([
                                                                    'flatpak-rpm-macros-0:29-6.module+125+c4f5c7f2.src',
                                                                    'flatpak-rpm-macros-0:29-6.module+125+c4f5c7f2.x86_64']), 
                      'flatpak-runtime-config-29-4.module+125+c4f5c7f2': set([
                                                                        'flatpak-runtime-config-0:29-4.module+125+c4f5c7f2.src',
                                                                        'flatpak-runtime-config-0:29-4.module+125+c4f5c7f2.x86_64'])}}
        self.assertEqual(data, expected)
        return

    def test_get_rpms_data_unknown_variant(self, fetch_json):
        fetch_json.return_value = RPMS_JSON
        msg = 'The http://localhost/compose/metadata/rpms.json does not contain payload -> rpms -> Workstation section'
        with six.assertRaisesRegex(self, ValueError, msg):
            compose = PungiCompose('http://localhost/compose/Workstation')
            compose.get_rpms_data()