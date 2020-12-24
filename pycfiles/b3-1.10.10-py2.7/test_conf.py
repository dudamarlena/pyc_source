# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\spree\test_conf.py
# Compiled at: 2016-03-08 18:42:10
from textwrap import dedent
from mock import Mock, call
from tests.plugins.spree import SpreeTestCase

class Test_killingspree_messages(SpreeTestCase):

    def setUp(self):
        SpreeTestCase.setUp(self)
        self.p.warning = Mock()

    def test_nominal(self):
        self.init(dedent("\n            [settings]\n            reset_spree: yes\n\n            [killingspree_messages]\n            # The # character splits the 'start' spree from the 'end' spree.\n            5: %player% is on a killing spree (5 kills in a row) # %player% stopped the spree of %victim%\n\n            [loosingspree_messages]\n            7: Keep it up %player%, it will come eventually # You're back in business %player%\n        "))
        self.assertListEqual([], self.p.warning.mock_calls)

    def test_no_message(self):
        self.init(dedent("\n            [settings]\n            reset_spree: yes\n\n            [killingspree_messages]\n\n            [loosingspree_messages]\n            7: Keep it up %player%, it will come eventually # You're back in business %player%\n        "))
        self.assertListEqual([], self.p.warning.mock_calls)

    def test_missing_dash(self):
        self.init(dedent("\n            [settings]\n            reset_spree: yes\n\n            [killingspree_messages]\n            # The # character splits the 'start' spree from the 'end' spree.\n            5: foo\n\n            [loosingspree_messages]\n            7: Keep it up %player%, it will come eventually # You're back in business %player%\n        "))
        self.assertListEqual([call("ignoring killingspree message 'foo' due to missing '#'")], self.p.warning.mock_calls)


class Test_loosingspree_messages(SpreeTestCase):

    def setUp(self):
        SpreeTestCase.setUp(self)
        self.p.warning = Mock()

    def test_nominal(self):
        self.init(dedent("\n            [settings]\n            reset_spree: yes\n\n            [killingspree_messages]\n\n            [loosingspree_messages]\n            # The # character splits the 'start' spree from the 'end' spree.\n            7: Keep it up %player%, it will come eventually # You're back in business %player%\n        "))
        self.assertListEqual([], self.p.warning.mock_calls)

    def test_no_message(self):
        self.init(dedent('\n            [settings]\n            reset_spree: yes\n\n            [killingspree_messages]\n\n            [loosingspree_messages]\n        '))
        self.assertListEqual([], self.p.warning.mock_calls)

    def test_missing_dash(self):
        self.init(dedent("\n            [settings]\n            reset_spree: yes\n\n            [killingspree_messages]\n\n            [loosingspree_messages]\n            # The # character splits the 'start' spree from the 'end' spree.\n            7: bar\n        "))
        self.assertListEqual([call("ignoring killingspree message 'bar' due to missing '#'")], self.p.warning.mock_calls)