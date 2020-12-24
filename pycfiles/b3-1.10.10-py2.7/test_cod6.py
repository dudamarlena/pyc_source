# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\core\parsers\test_cod6.py
# Compiled at: 2016-03-08 18:42:10
import logging
from mock import Mock
from mockito import mock, when, any as anything
import unittest2 as unittest
from b3.clients import Client
from b3.config import XmlConfigParser
from b3.parsers.cod6 import Cod6Parser
log = logging.getLogger('test')
log.setLevel(logging.INFO)
original_client_auth = Client.auth

def tearDownModule():
    Client.auth = original_client_auth


class Cod6TestCase(unittest.TestCase):
    """
    Test case that is suitable for testing Cod6 parser specific features
    """

    @classmethod
    def setUpClass(cls):
        from b3.parsers.q3a.abstractParser import AbstractParser
        from b3.fake import FakeConsole
        AbstractParser.__bases__ = (FakeConsole,)
        logging.getLogger('output').setLevel(logging.ERROR)

    def setUp(self):
        self.parser_conf = XmlConfigParser()
        self.parser_conf.loadFromString('<configuration>\n                <settings name="server">\n                    <set name="game_log"/>\n                </settings>\n            </configuration>')
        self.console = Cod6Parser(self.parser_conf)
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


class Test_parser_API(Cod6TestCase):

    def test_getPlayerList_without_punkbuster(self):
        self.console.PunkBuster = None
        when(self.console).write('status', maxRetries=anything()).thenReturn('map: mp_highrise\nnum score ping guid                             name            lastmsg address               qport rate\n--- ----- ---- -------------------------------- --------------- ------- --------------------- ----- -----\n  0     1   69                 011000010002d113 Minikruku!^7            0 11.11.11.11:16864    20125 25000\n  1     1  101                 011000010002caf1 GuMaK111^7             50 11.11.11.11:4294934838  690 25000\n  2     1  175                 0110000100003fb4 phantom1151^7           0 11.11.11.11:28960    10929 25000\n  3     1   49                 011000010003ed88 isidora10^7             0 11.11.11.11:429496262727388 25000\n  4     1   31                 011000018e87f252 [^5RnK^0] ^4B^7              50 11.11.11.11:28960  26213 25000\n')
        rv = self.console.getPlayerList()
        self.assertDictContainsSubset({'slot': '0', 
           'score': '1', 'ping': '69', 'guid': '011000010002d113', 'name': 'Minikruku!^7', 'last': '0', 'ip': '11.11.11.11', 'pbid': None}, rv.get('0', {}))
        self.assertDictContainsSubset({'slot': '1', 
           'score': '1', 'ping': '101', 'guid': '011000010002caf1', 'name': 'GuMaK111^7', 'last': '50', 'ip': '11.11.11.11', 'pbid': None}, rv.get('1', {}))
        self.assertDictContainsSubset({'slot': '2', 
           'score': '1', 'ping': '175', 'guid': '0110000100003fb4', 'name': 'phantom1151^7', 'last': '0', 'ip': '11.11.11.11', 'pbid': None}, rv.get('2', {}))
        self.assertDictContainsSubset({'slot': '3', 
           'score': '1', 'ping': '49', 'guid': '011000010003ed88', 'name': 'isidora10^7', 'last': '0', 'ip': '11.11.11.11', 'pbid': None}, rv.get('3', {}))
        self.assertDictContainsSubset({'slot': '4', 
           'score': '1', 'ping': '31', 'guid': '011000018e87f252', 'name': '[^5RnK^0] ^4B^7', 'last': '50', 'ip': '11.11.11.11', 'pbid': None}, rv.get('4', {}))
        return