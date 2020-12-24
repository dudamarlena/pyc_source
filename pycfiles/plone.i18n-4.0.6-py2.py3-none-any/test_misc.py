# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/matej/workarea/plone.hud/plone.hud1/src/plone/hud/tests/test_misc.py
# Compiled at: 2013-09-14 11:12:12
__doc__ = 'Test misc functions in misc.py file.'
from plone.hud.misc import normalize_name
from plone.hud.misc import get_panel_id
import unittest2

class TestMisc(unittest2.TestCase):

    def test_normalize_name(self):
        self.assertEqual(normalize_name('Users Panel'), 'users_panel')
        self.assertEqual(normalize_name('Users_Panel'), 'users_panel')

    def test_get_panel_id(self):
        self.assertEqual(get_panel_id('Users Panel'), 'hud_users_panel')
        self.assertEqual(get_panel_id('Users_Panel'), 'hud_users_panel')