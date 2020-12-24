# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: H:\workspaces\workspace-python\big-brother-bot\tests\plugins\test_ftpytail.py
# Compiled at: 2015-02-24 17:29:43
from tests import B3TestCase
from b3.plugins.ftpytail import FtpytailPlugin

class FtpytailPluginTestCase(B3TestCase):

    def test_load_plugin(self):
        p = FtpytailPlugin(self.console)
        p.onLoadConfig()