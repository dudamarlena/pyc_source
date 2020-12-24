# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/aws_sudo/testCommandParser.py
# Compiled at: 2017-08-31 10:35:10
import CommandParser, unittest

class TestCommandParser(unittest.TestCase):

    def setUp(self):
        self.parser = CommandParser.CommandParser()

    def test_defaults(self):
        args = self.parser.get_arguments(('aws-sudo test-profile test-command').split()[1:])
        self.assertEqual(args.mfa_code, None)
        self.assertEqual(args.session_timeout, 3600)
        return

    def test_export_mode_when_no_command(self):
        args = self.parser.get_arguments(('aws-sudo test-profile').split()[1:])
        self.assertEqual(args.mode, 'export')

    def test_duplicated_parameters(self):
        args = self.parser.get_arguments(('aws-sudo -m 123 test-profile test-command -m 321').split()[1:])
        self.assertEqual(args.mfa_code, '123')
        self.assertEqual(args.command_args, ['-m', '321'])
        args = self.parser.get_arguments(('aws-sudo -m 123 -s 3600 test-profile test-command -m 321 -s 10').split()[1:])
        self.assertEqual(args.mfa_code, '123')
        self.assertEqual(args.session_timeout, 3600)
        self.assertEqual(args.command_args, ['-m', '321', '-s', '10'])

    def test_in_place(self):
        args = self.parser.get_arguments(('aws-sudo -i -s 3600 test-profile test-command').split()[1:])
        self.assertEqual(args.mode, 'in_place')
        args = self.parser.get_arguments(('aws-sudo -i test-profile test-command -i').split()[1:])
        self.assertEqual(args.mode, 'in_place')
        args = self.parser.get_arguments(('aws-sudo -i test-profile').split()[1:])
        self.assertEqual(args.mode, 'in_place')
        args = self.parser.get_arguments(('aws-sudo test-profile test-command -i lorem').split()[1:])
        self.assertEqual(args.mode, 'proxy')
        args = self.parser.get_arguments(('aws-sudo test-profile test-command -i').split()[1:])
        self.assertEqual(args.mode, 'proxy')


if __name__ == '__main__':
    unittest.main()