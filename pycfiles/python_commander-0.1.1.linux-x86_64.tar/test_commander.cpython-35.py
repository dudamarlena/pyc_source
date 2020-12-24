# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/enthys/workspace/python/python_commander/venv/lib/python3.5/site-packages/python_commander/tests/test_commander.py
# Compiled at: 2018-10-31 08:00:25
# Size of source mod 2**32: 1085 bytes
import unittest
from .. import Commander

class CommanderTest(unittest.TestCase):

    def setUp(self):
        Commander.commands = []

    def test_giving_command_to_commander(self):
        Commander.command('test', 'echo "Hello"')
        self.assertEqual(len(Commander.commands), 1)

    def test_action_is_added_in_correct_format(self):
        Commander.command('test', 'echo "Hello"')
        self.assertListEqual(Commander.commands, [
         {'command': 'test', 
          'action': 'echo "Hello"', 
          'description': ''}])

    def test_passing_function_to_commander_as_action(self):

        def fake_function():
            return 'Foo'

        Commander.command('test', fake_function)
        self.assertTrue(hasattr(Commander.commands[0]['action'], '__call__'))
        self.assertEqual(Commander.take_action(['filler', 'test']), 'Foo')

    def test_shell_command_returns_value(self):
        Commander.command('test', 'echo Hello')
        self.assertEqual(Commander.take_action(['filler', 'test']), 'Hello')