# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/matej/workarea/plone.hud/plone.hud1/src/plone/hud/tests/test_panel.py
# Compiled at: 2013-09-14 11:09:16
__doc__ = 'Tests for utils in this package.'
from plone.hud import register_hud_panel
from plone.hud.testing import IntegrationTestCase
import mock

class TestPanel(IntegrationTestCase):
    """Integration tests for panel."""

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.panel = self.portal.unrestrictedTraverse('@@hud')

    def prepare_panel_env(self, request_form={}):
        """Prepare all the variables for various tests.

        Also, optionally you can set 'request_form' (it must be dict type),
        this updates the values in the view.request.form,
        it does not remove any keys.
        """
        with mock.patch('plone.hud.panel.HUDPanelView.main_template'):
            self.panel.request.form.update(request_form)
            self.panel.render()

    def test_get_panels(self):
        register_hud_panel('Sheeps')
        register_hud_panel('Goats')
        register_hud_panel('Cats')
        register_hud_panel('Dogs')
        self.prepare_panel_env()
        self.panel.portal.restrictedTraverse = mock.Mock()
        self.panel.portal.restrictedTraverse.return_value.title = 'Mocked Title'
        self.assertEqual(self.panel.get_panels(), [
         {'url': 'http://nohost/plone/@@hud?panel_name=hud_cats', 
            'name': 'hud_cats', 
            'title': 'Mocked Title'},
         {'url': 'http://nohost/plone/@@hud?panel_name=hud_dogs', 
            'name': 'hud_dogs', 
            'title': 'Mocked Title'},
         {'url': 'http://nohost/plone/@@hud?panel_name=hud_goats', 
            'name': 'hud_goats', 
            'title': 'Mocked Title'},
         {'url': 'http://nohost/plone/@@hud?panel_name=hud_sheeps', 
            'name': 'hud_sheeps', 
            'title': 'Mocked Title'}])