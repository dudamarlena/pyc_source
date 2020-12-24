# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\core\parsers\test_et.py
# Compiled at: 2016-03-08 18:42:10
import logging, StringIO
from mock import call, patch, Mock
from mockito import mock, verify
import unittest2 as unittest
from b3.clients import Client
from b3.config import XmlConfigParser
from b3.parsers.et import EtParser
log = logging.getLogger('test')
log.setLevel(logging.INFO)

class EtTestCase(unittest.TestCase):
    """
    Test case that is suitable for testing et parser specific features
    """

    @classmethod
    def setUpClass(cls):
        from b3.parsers.q3a.abstractParser import AbstractParser
        from b3.fake import FakeConsole
        AbstractParser.__bases__ = (
         FakeConsole,)
        logging.getLogger('output').setLevel(logging.ERROR)

    def setUp(self):
        self.parser_conf = XmlConfigParser()
        self.parser_conf.loadFromString('<configuration>\n                <settings name="server">\n                    <set name="game_log"/>\n                </settings>\n            </configuration>')
        self.console = EtParser(self.parser_conf)
        self.console.write = Mock()
        self.console.PunkBuster = None
        return

    def tearDown(self):
        if hasattr(self, 'parser'):
            del self.parser.clients
            self.parser.working = False


class Test_parser_API_implementation(EtTestCase):
    """Test case that is responsible for testing all methods of the b3.parser.Parser class API that
    have to override because they have to talk to their targeted game server in their specific way"""

    def test_say(self):
        self.console.msgPrefix = 'B3:'
        self.console.say('something')
        self.console.msgPrefix = None
        self.console.say('something else')
        self.assertListEqual(self.console.write.mock_calls, [call('qsay B3: something'),
         call('qsay something else')])
        return

    def test_saybig(self):
        self.console.msgPrefix = 'B3:'
        self.console.saybig('something')
        self.console.msgPrefix = None
        self.console.saybig('something else')
        self.assertListEqual(self.console.write.mock_calls, [call('qsay B3: ^1something'),
         call('qsay B3: ^2something'),
         call('qsay B3: ^3something'),
         call('qsay B3: ^4something'),
         call('qsay B3: ^5something'),
         call('qsay ^1something else'),
         call('qsay ^2something else'),
         call('qsay ^3something else'),
         call('qsay ^4something else'),
         call('qsay ^5something else')])
        return

    def test_message(self):
        superman = Client(console=self.console, cid='11')
        self.console.msgPrefix = 'B3:'
        self.console.pmPrefix = '^3[pm]^7'
        self.console.message(superman, 'something')
        self.console.msgPrefix = None
        self.console.pmPrefix = None
        self.console.message(superman, 'something else')
        self.assertListEqual(self.console.write.mock_calls, [call('qsay B3: ^3[pm]^7 something'),
         call('qsay something else')])
        return