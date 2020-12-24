# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hanzz/releases/odcs/server/tests/test_pungi.py
# Compiled at: 2017-08-31 11:17:14
# Size of source mod 2**32: 2504 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, unittest
from mock import patch
from odcs.server.pungi import Pungi, PungiConfig, PungiSourceType

class TestPungiConfig(unittest.TestCase):

    def setUp(self):
        pass

    def test_pungi_config_module(self):
        pungi_cfg = PungiConfig('MBS-512', '1', PungiSourceType.MODULE, 'testmodule-master')
        pungi_cfg.get_pungi_config()
        variants = pungi_cfg.get_variants_config()
        comps = pungi_cfg.get_comps_config()
        self.assertTrue(variants.find('<module>') != -1)
        self.assertEqual(comps, '')

    def test_pungi_config_tag(self):
        pungi_cfg = PungiConfig('MBS-512', '1', PungiSourceType.KOJI_TAG, 'f26', packages=['file'])
        pungi_cfg.get_pungi_config()
        variants = pungi_cfg.get_variants_config()
        comps = pungi_cfg.get_comps_config()
        self.assertTrue(variants.find('<groups>') != -1)
        self.assertTrue(comps.find('file</packagereq>') != -1)


class TestPungi(unittest.TestCase):

    def setUp(self):
        pass

    @patch('odcs.server.utils.execute_cmd')
    def test_pungi_run(self, execute_cmd):
        pungi_cfg = PungiConfig('MBS-512', '1', PungiSourceType.MODULE, 'testmodule-master')
        pungi = Pungi(pungi_cfg)
        pungi.run()
        execute_cmd.assert_called_once()