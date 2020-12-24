# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ajdiaz/env/drove/lib/python3.4/site-packages/drove/tests/test_command.py
# Compiled at: 2015-01-20 05:42:58
# Size of source mod 2**32: 297 bytes
import unittest
from drove.command import Command

class TestCommand(unittest.TestCase):

    def test_command(self):
        cmd = Command.from_name('list', None, None, None)
        assert cmd.__class__.__name__ == 'ListCommand'