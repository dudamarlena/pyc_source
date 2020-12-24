# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mmonroy/Desktop/data/num2words/tests/test_cli.py
# Compiled at: 2020-04-17 01:12:12
from __future__ import unicode_literals
import os, unittest, delegator, numinwords

class CliCaller(object):

    def __init__(self):
        self.cmd = os.path.realpath(os.path.join(os.path.dirname(__file__), b'..', b'bin', b'numinwords'))
        self.cmd_list = [b'python', self.cmd]

    def run_cmd(self, *args):
        cmd_list = self.cmd_list + [ str(arg) for arg in args ]
        cmd = (b' ').join(cmd_list)
        return delegator.run(cmd)


class CliTestCase(unittest.TestCase):
    """Test the command line app"""

    def setUp(self):
        self.cli = CliCaller()

    def test_cli_help(self):
        """numinwords without arguments should exit with status 1
        and show docopt's default short usage message
        """
        output = self.cli.run_cmd()
        self.assertEqual(output.return_code, 1)
        self.assertTrue(output.err.startswith(b'Usage:'))

    def test_cli_list_langs(self):
        """You should be able to list all availabe languages
        """
        output = self.cli.run_cmd(b'--list-languages')
        self.assertEqual(sorted(list(numinwords.CONVERTER_CLASSES.keys())), output.out.strip().split(os.linesep))
        output = self.cli.run_cmd(b'-L')
        self.assertEqual(sorted(list(numinwords.CONVERTER_CLASSES.keys())), output.out.strip().split(os.linesep))

    def test_cli_list_converters(self):
        """You should be able to list all available converters
        """
        output = self.cli.run_cmd(b'--list-converters')
        self.assertEqual(sorted(list(numinwords.CONVERTES_TYPES)), output.out.strip().split(os.linesep))
        output = self.cli.run_cmd(b'-C')
        self.assertEqual(sorted(list(numinwords.CONVERTES_TYPES)), output.out.strip().split(os.linesep))

    def test_cli_default_lang(self):
        """Default to english
        """
        output = self.cli.run_cmd(150)
        self.assertEqual(output.return_code, 0)
        self.assertEqual(output.out.strip(), b'one hundred and fifty')

    def test_cli_with_lang(self):
        """You should be able to specify a language
        """
        output = self.cli.run_cmd(150, b'--lang', b'es')
        self.assertEqual(output.return_code, 0)
        self.assertEqual(output.out.strip(), b'ciento cincuenta')

    def test_cli_with_lang_to(self):
        """You should be able to specify a language and currency
        """
        output = self.cli.run_cmd(150.55, b'--lang', b'es', b'--to', b'currency')
        self.assertEqual(output.return_code, 0)
        self.assertEqual((output.out.decode(b'utf-8') if hasattr(output.out, b'decode') else output.out).strip(), b'ciento cincuenta euros con cincuenta y cinco céntimos')