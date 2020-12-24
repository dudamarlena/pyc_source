# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\core\parsers\test_cod4gr.py
# Compiled at: 2016-03-08 18:42:10
import logging, unittest2 as unittest
from mock import Mock, patch, ANY
from mockito import mock, when, any as anything
from b3.clients import Client
from b3.config import XmlConfigParser
from b3.fake import FakeClient
from b3.parsers.cod4gr import Cod4grParser
log = logging.getLogger('test')
log.setLevel(logging.INFO)
original_client_auth = Client.auth

def tearDownModule():
    Client.auth = original_client_auth


class Cod4grTestCase(unittest.TestCase):
    """
    Test case that is suitable for testing Cod4gr parser specific features
    """

    @classmethod
    def setUpClass(cls):
        from b3.parsers.q3a.abstractParser import AbstractParser
        from b3.fake import FakeConsole
        AbstractParser.__bases__ = (FakeConsole,)

    def setUp(self):
        self.parser_conf = XmlConfigParser()
        self.parser_conf.loadFromString('<configuration>\n                <settings name="server">\n                    <set name="game_log"/>\n                </settings>\n            </configuration>')
        self.console = Cod4grParser(self.parser_conf)
        self.output_mock = mock()

        def write(*args, **kwargs):
            pretty_args = map(repr, args) + [ '%s=%s' % (k, v) for k, v in kwargs.iteritems() ]
            log.info('write(%s)' % (', ').join(pretty_args))
            return self.output_mock.write(*args, **kwargs)

        self.console.write = Mock(wraps=write)
        self.player = self.console.clients.newClient(cid='4', guid='theGuid', name='theName', ip='11.22.33.44')

    def tearDown(self):
        if hasattr(self, 'parser'):
            del self.parser.clients
            self.parser.working = False


class Test_parser_API(Cod4grTestCase):

    def test_getPlayerList_without_punkbuster(self):
        self.console.PunkBuster = None
        when(self.console).write('status', maxRetries=anything()).thenReturn('\nmap: mp_backlot\nnum score ping guid                             name            lastmsg address               qport rate\n--- ----- ---- -------------------------------- --------------- ------- --------------------- ----- -----\n  0     0    3 GameRanger-Account-ID_0006400896 Ranger^7             50 103.231.162.141:16000  7068 25000\n')
        rv = self.console.getPlayerList()
        self.assertDictEqual({'slot': '0', 'score': '0', 'ping': '3', 'guid': '0006400896', 'name': 'Ranger^7', 'last': '50', 'ip': '103.231.162.141', 'port': '16000', 'qport': '7068', 'rate': '25000', 'pbid': None}, rv.get('0', {}), rv)
        return