# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nih/Projekte/_qa/paci/tests/commands/test_configure.py
# Compiled at: 2017-04-10 05:52:50
# Size of source mod 2**32: 949 bytes
"""Tests for our `configure` command."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, unittest
from unittest.mock import patch, mock_open
from docopt import docopt
from io import StringIO
import paci.cli
from paci.commands.configure import Configure
doc = paci.__doc__

class TestConfigure(unittest.TestCase):

    def test_prints_the_welcome_msg(self):
        configure = Configure(['test'])
        with patch('sys.stdout', new_callable=StringIO) as (sysout):
            with patch('paci.commands.configure.input', return_value=False) as (m):
                configure.run()
        self.assertIn('Lets configure a new settings.yml for paci!', sysout.getvalue())

    def test_asks_for_basedir(self):
        configure = Configure(['test'])
        with patch('sys.stdout', new_callable=StringIO) as (sysout):
            with patch('sys.stdin', new_callable=StringIO) as (sysin):
                configure.run()
        self.assertIn('basedir (defaults to', sysin.getvalue())