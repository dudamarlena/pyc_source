# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/code/pyutil/pyutil/test/current/test_passphrase.py
# Compiled at: 2018-01-14 07:59:35
# Size of source mod 2**32: 1964 bytes
import unittest
from io import BytesIO
from mock import patch, call, ANY
from pyutil.scripts import passphrase

class Passphrase(unittest.TestCase):

    @patch('argparse.ArgumentParser')
    @patch('pyutil.scripts.passphrase.gen_passphrase')
    @patch('sys.stdout')
    @patch('sys.stderr')
    def test_main(self, m_stderr, m_stdout, m_gen_passphrase, m_ArgumentParser):
        m_args = m_ArgumentParser.return_value.parse_args.return_value
        m_args.dictionary = BytesIO(b'alpha\nbeta\n')
        m_args.bits = 42
        m_gen_passphrase.return_value = ('wombat', 43)
        passphrase.main()
        self.assertEqual(m_ArgumentParser.mock_calls, [
         call(prog='passphrase', description='Create a random passphrase by ' + 'picking a few random words.'),
         call().add_argument('-d', '--dictionary', help='what file to read a list of words from ' + "(or omit this option to use passphrase's " + 'bundled dictionary)', type=ANY, metavar='DICT'),
         call().add_argument('bits', help='how many bits of entropy minimum', type=float, metavar='BITS'),
         call().parse_args()])
        self.assertEqual(m_gen_passphrase.mock_calls, [
         call(42, {'alpha', 'beta'})])
        self.assertEqual(m_stdout.mock_calls, [
         call.write('wombat'),
         call.write('\n')])
        self.assertEqual(m_stderr.mock_calls, [
         call.write('This passphrase encodes about 43 bits.\n')])