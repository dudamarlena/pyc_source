# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/rbtools/commands/tests/test_main.py
# Compiled at: 2020-04-14 20:27:46
"""Tests for RBTools help command and rbt command help options."""
from __future__ import unicode_literals
from rbtools.utils.process import execute
from rbtools.utils.testbase import RBTestBase

class HelpCommandTests(RBTestBase):
    """Tests for RBT help command and rbt command help options."""

    def test_help_command(self):
        """Testing RBT commands when running 'rbt help <command>'"""
        self._check_help_output([b'rbt', b'help', b'alias'], b'alias')

    def test_help_options_before(self):
        """Testing RBT commands when running 'rbt --help <command>' or 'rbt
        -h <command>'
        """
        self._check_help_output([b'rbt', b'--help', b'alias'], b'alias')
        self._check_help_output([b'rbt', b'-h', b'alias'], b'alias')

    def test_help_options_after(self):
        """Testing RBT commands when running 'rbt <command> --help' or 'rbt
        <command> -h'
         """
        self._check_help_output([b'rbt', b'alias', b'--help'], b'alias')
        self._check_help_output([b'rbt', b'alias', b'-h'], b'alias')

    def test_help_invalid_command(self):
        """Testing RBT commands when running '--help' or '-h' with an
        invalid command
         """
        self._check_help_output([b'rbt', b'invalid', b'--help'], b'invalid', invalid=True)
        self._check_help_output([b'rbt', b'invalid', b'-h'], b'invalid', invalid=True)
        self._check_help_output([b'rbt', b'help', b'invalid'], b'invalid', invalid=True)

    def test_help_multiple_args(self):
        """Testing RBT commands when running the help command or help
        options with multiple arguments present
        """
        self._check_help_output([b'rbt', b'alias', b'extra_arg', b'--help'], b'alias')
        self._check_help_output([b'rbt', b'alias', b'extra_arg', b'-h'], b'alias')
        self._check_help_output([b'rbt', b'alias', b'--help', b'extra_arg'], b'alias')
        self._check_help_output([b'rbt', b'alias', b'-h', b'extra_arg'], b'alias')
        self._check_help_output([b'rbt', b'--help', b'alias', b'extra_arg'], b'alias')
        self._check_help_output([b'rbt', b'-h', b'alias', b'extra_arg'], b'alias')
        self._check_help_output([b'rbt', b'help', b'alias', b'extra_arg'], b'alias')

    def _check_help_output(self, command, subcommand, invalid=False):
        """Check if a specific rbt command's output exists in test output.

        Args:
            command (list of unicode):
                The rbt command used for testing.

            subcommand (unicode)
                The unicode string of the rbt command type.

            invalid (bool, optional):
                If ``True``, check if output matches what is expected after
                running an invalid command. Otherwise, check if output
                matches what is expected after running a valid rbt command.
        """
        try:
            output = execute(command)
        except Exception as e:
            self.fail(e)

        if invalid:
            self.assertIn(b'No help found for %s' % subcommand, output)
        else:
            self.assertIn(b'usage: rbt %s [options]' % subcommand, output)