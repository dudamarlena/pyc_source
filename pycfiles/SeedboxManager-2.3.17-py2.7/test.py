# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-1.7.35-i686/egg/seedbox/tests/test.py
# Compiled at: 2015-06-14 13:30:57
"""Common utilities used in testing"""
import os, shutil, tempfile
from oslo_config import fixture as config
from oslotest import base
BaseTestCase = base.BaseTestCase

class ConfiguredBaseTestCase(BaseTestCase):

    def setUp(self):
        super(ConfiguredBaseTestCase, self).setUp()
        self.CONF = self.useFixture(config.Config()).conf
        self.CONF.import_group('torrent', 'seedbox.torrent')
        self.base_dir = tempfile.gettempdir()
        self.set_required_options()
        self.CONF([], project='seedbox')
        self.CONF.set_override('config_dir', self.base_dir)
        if self.base_dir != self.CONF.config_dir:
            self.CONF.set_default('config_dir', self.base_dir)

    def tearDown(self):
        shutil.rmtree(self.base_dir, ignore_errors=True)
        self.CONF.reset()
        super(ConfiguredBaseTestCase, self).tearDown()

    def _make_dir(self, dirname):
        dirpath = os.path.join(self.base_dir, dirname)
        os.mkdir(dirpath)
        return dirpath

    def set_required_options(self):
        self.CONF.set_override('torrent_path', self._make_dir('torrent'), group='torrent')
        self.CONF.set_override('media_paths', [
         self._make_dir('complete'),
         self._make_dir('seedLT')], group='torrent')
        self.CONF.set_override('incomplete_path', self._make_dir('inprogress'), group='torrent')