# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/action_testcases.py
# Compiled at: 2011-10-28 19:16:45
from unittest import TestCase
from hgwebcommit.actions import FunctionAction, ActionManager
__all__ = [
 'ActionTestCase', 'ActionManagerTestCase']

class ActionTestCase(TestCase):
    """
    Actionのテスト
    """

    def test_call(self):
        action = FunctionAction('test', 'test', lambda : 'ok')
        self.assertEqual(action(), 'ok')


class ActionManagerTestCase(TestCase):
    """
    ActionManagerのテスト
    """

    def setUp(self):
        self.action = FunctionAction('test', 'test', lambda : 'ok')
        self.manager = ActionManager()

    def test_add(self):
        self.manager.add(self.action)
        self.assertEqual(len(self.manager.actions), 1)

    def test_call(self):
        self.manager.add(self.action)
        self.assertEqual(self.manager.call('test'), 'ok')