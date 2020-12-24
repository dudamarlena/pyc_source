# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\core\parsers\homefront\test_HomefrontParser.py
# Compiled at: 2016-03-08 18:42:10
from b3.parsers.homefront import HomefrontParser
from mock import Mock, sentinel
import b3, unittest2 as unittest

class Test_HomefrontParser(unittest.TestCase):

    def setUp(self):
        self.mock_parser = Mock(spec=HomefrontParser)
        self.mock_parser._reSteamId64 = HomefrontParser._reSteamId64
        self.mock_parser.onServerKill = HomefrontParser.onServerKill
        self.courgette = Mock(spec=b3.clients.Client, name='courgette')
        self.freelander = Mock(spec=b3.clients.Client, name='freelander')

        def getClient(name):
            if name == 'courgette':
                return self.courgette
            else:
                if name == 'Freelander':
                    return self.freelander
                return Mock(spec=b3.clients.Client)

        self.mock_parser.getClient = getClient

        def getByGUID(guid):
            if guid == '12311111111111111':
                return self.courgette
            else:
                if guid == '12300000000000000':
                    return self.freelander
                return Mock(spec=b3.clients.Client)

        self.mock_parser.clients.getByGUID = getByGUID

    def tearDown(self):
        if hasattr(self, 'parser'):
            del self.parser.clients
            self.parser.working = False

    def test_unmeaningful_data(self):
        self.assertIsNone(self.mock_parser.onServerKill(self.mock_parser, 'qsdf'))

    def test_teamkill_with_names(self):
        self.mock_parser.reset_mock()
        self.courgette.team = self.freelander.team = sentinel.DEFAULT
        self.mock_parser.onServerKill(self.mock_parser, 'courgette EXP_Frag Freelander')
        self.assertTrue(self.mock_parser.getEvent.called)
        getEvent_args = self.mock_parser.getEvent.call_args[0]
        self.assertEqual('EVT_CLIENT_KILL_TEAM', getEvent_args[0])
        self.assertEqual('EXP_Frag', getEvent_args[1][1])
        self.assertEqual(self.courgette, getEvent_args[2])
        self.assertEqual(self.freelander, getEvent_args[3])

    def test_teamkill_with_steamid(self):
        self.mock_parser.reset_mock()
        self.courgette.team = self.freelander.team = sentinel.DEFAULT
        self.mock_parser.onServerKill(self.mock_parser, '12311111111111111 EXP_Frag 12300000000000000')
        self.assertTrue(self.mock_parser.getEvent.called)
        getEvent_args = self.mock_parser.getEvent.call_args[0]
        self.assertEqual('EVT_CLIENT_KILL_TEAM', getEvent_args[0])
        self.assertEqual('EXP_Frag', getEvent_args[1][1])
        self.assertEqual(self.courgette, getEvent_args[2])
        self.assertEqual(self.freelander, getEvent_args[3])

    def test_kill_with_names(self):
        self.mock_parser.reset_mock()
        self.mock_parser.onServerKill(self.mock_parser, 'courgette EXP_Frag Freelander')
        self.assertTrue(self.mock_parser.getEvent.called)
        getEvent_args = self.mock_parser.getEvent.call_args[0]
        self.assertEqual('EVT_CLIENT_KILL', getEvent_args[0])
        self.assertEqual('EXP_Frag', getEvent_args[1][1])
        self.assertEqual(self.courgette, getEvent_args[2])
        self.assertEqual(self.freelander, getEvent_args[3])

    def test_kill_with_steamid(self):
        self.mock_parser.reset_mock()
        self.mock_parser.onServerKill(self.mock_parser, '12311111111111111 EXP_Frag 12300000000000000')
        self.assertTrue(self.mock_parser.getEvent.called)
        getEvent_args = self.mock_parser.getEvent.call_args[0]
        self.assertEqual('EVT_CLIENT_KILL', getEvent_args[0])
        self.assertEqual('EXP_Frag', getEvent_args[1][1])
        self.assertEqual(self.courgette, getEvent_args[2])
        self.assertEqual(self.freelander, getEvent_args[3])

    def test_suicide_with_names(self):
        self.mock_parser.reset_mock()
        self.mock_parser.onServerKill(self.mock_parser, 'courgette EXP_Frag courgette')
        self.assertTrue(self.mock_parser.getEvent.called)
        getEvent_args = self.mock_parser.getEvent.call_args[0]
        self.assertEqual('EVT_CLIENT_SUICIDE', getEvent_args[0])
        self.assertEqual('EXP_Frag', getEvent_args[1][1])
        self.assertEqual(self.courgette, getEvent_args[2])
        self.assertEqual(self.courgette, getEvent_args[3])

    def test_suicide_with_steamid(self):
        self.mock_parser.reset_mock()
        self.mock_parser.onServerKill(self.mock_parser, '12311111111111111 EXP_Frag 12311111111111111')
        self.assertTrue(self.mock_parser.getEvent.called)
        getEvent_args = self.mock_parser.getEvent.call_args[0]
        self.assertEqual('EVT_CLIENT_SUICIDE', getEvent_args[0])
        self.assertEqual('EXP_Frag', getEvent_args[1][1])
        self.assertEqual(self.courgette, getEvent_args[2])
        self.assertEqual(self.courgette, getEvent_args[3])


if __name__ == '__main__':
    unittest.main()