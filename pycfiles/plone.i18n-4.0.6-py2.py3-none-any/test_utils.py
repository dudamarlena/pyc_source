# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/matej/workarea/plone.hud/plone.hud1/src/plone/hud/tests/test_utils.py
# Compiled at: 2013-09-14 10:22:22
__doc__ = 'Tests for utils in this package.'
from plone.hud import register_hud_panel
from plone.hud import unregister_hud_panel
from plone.hud.testing import IntegrationTestCase

class TestUtils(IntegrationTestCase):

    def test_register_panel_cycle(self):
        panel_name = 'Sheeps'
        panel_id = register_hud_panel(panel_name)
        self.assertEqual(panel_id, 'hud_sheeps')
        panel_id = unregister_hud_panel(panel_name)
        self.assertEqual(panel_id, 'hud_sheeps')