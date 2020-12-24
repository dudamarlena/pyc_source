# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/pbr/tests/test_hooks.py
# Compiled at: 2017-12-04 07:19:32
import os
from testtools import matchers
from pbr.tests import base
from pbr.tests import util

class TestHooks(base.BaseTestCase):

    def setUp(self):
        super(TestHooks, self).setUp()
        with util.open_config(os.path.join(self.package_dir, 'setup.cfg')) as (cfg):
            cfg.set('global', 'setup-hooks', 'pbr_testpackage._setup_hooks.test_hook_1\npbr_testpackage._setup_hooks.test_hook_2')

    def test_global_setup_hooks(self):
        """Test setup_hooks.

        Test that setup_hooks listed in the [global] section of setup.cfg are
        executed in order.
        """
        stdout, _, return_code = self.run_setup('egg_info')
        assert 'test_hook_1\ntest_hook_2' in stdout
        assert return_code == 0

    def test_custom_commands_known(self):
        stdout, _, return_code = self.run_setup('--help-commands')
        self.assertFalse(return_code)
        self.assertThat(stdout, matchers.Contains(' testr '))