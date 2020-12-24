# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/matej/workarea/plone.hud/plone.hud1/src/plone/hud/tests/test_misc.py
# Compiled at: 2013-09-14 11:12:12
"""Test misc functions in misc.py file."""
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