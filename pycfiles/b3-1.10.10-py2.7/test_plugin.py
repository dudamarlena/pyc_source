# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\publist\test_plugin.py
# Compiled at: 2016-03-08 18:42:10
from tests import B3TestCase
from b3.plugins.publist import PublistPlugin

class PublistPluginTestCase(B3TestCase):

    def test_load_plugin(self):
        p = PublistPlugin(self.console)
        p.onLoadConfig()
        p.onStartup()