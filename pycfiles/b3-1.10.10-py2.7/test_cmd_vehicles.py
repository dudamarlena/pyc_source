# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\poweradminbf3\test_cmd_vehicles.py
# Compiled at: 2016-03-08 18:42:10
from mock import Mock
from b3.config import CfgConfigParser
from b3.cvar import Cvar
from b3.parsers.frostbite2.protocol import CommandFailedError
from b3.plugins.poweradminbf3 import Poweradminbf3Plugin
from tests.plugins.poweradminbf3 import Bf3TestCase

class Test_cmd_vehicles(Bf3TestCase):

    def setUp(self):
        Bf3TestCase.setUp(self)
        self.conf = CfgConfigParser()
        self.conf.loadFromString('[commands]\nvehicles: 20\n        ')
        self.p = Poweradminbf3Plugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()

    def test_no_argument_true(self):

        def getCvar_proxy(var_name):
            if var_name == 'vehicleSpawnAllowed':
                return Cvar('vehicleSpawnAllowed', value='true')
            else:
                return Mock()

        self.p.console.getCvar = Mock(side_effect=getCvar_proxy)
        self.moderator.connects('moderator')
        self.moderator.message_history = []
        self.moderator.says('!vehicles')
        self.assertEqual(1, len(self.moderator.message_history))
        self.assertEqual('Vehicle spawn is [ON]', self.moderator.message_history[0])

    def test_no_argument_false(self):

        def getCvar_proxy(var_name):
            if var_name == 'vehicleSpawnAllowed':
                return Cvar('vehicleSpawnAllowed', value='false')
            else:
                return Mock()

        self.p.console.getCvar = Mock(side_effect=getCvar_proxy)
        self.moderator.connects('moderator')
        self.moderator.message_history = []
        self.moderator.says('!vehicles')
        self.assertEqual(1, len(self.moderator.message_history))
        self.assertEqual('Vehicle spawn is [OFF]', self.moderator.message_history[0])

    def test_no_argument_error(self):

        def getCvar_proxy(var_name):
            if var_name == 'vehicleSpawnAllowed':
                raise CommandFailedError(['foo'])
            else:
                return Mock()

        self.p.console.getCvar = Mock(side_effect=getCvar_proxy)
        self.moderator.connects('moderator')
        self.moderator.message_history = []
        self.moderator.says('!vehicles')
        self.assertEqual(1, len(self.moderator.message_history))
        self.assertEqual('Vehicle spawn is [unknown]', self.moderator.message_history[0])

    def test_with_argument_foo(self):

        def setCvar_proxy(var_name, value):
            if var_name == 'vehicleSpawnAllowed':
                raise CommandFailedError(['InvalidArguments'])
            else:
                return Mock()

        self.p.console.setCvar = Mock(side_effect=setCvar_proxy)
        self.p.console.getCvar = Mock(return_value='bar')
        self.moderator.connects('moderator')
        self.moderator.message_history = []
        self.moderator.says('!vehicles foo')
        self.assertIn("unexpected value 'foo'. Available modes : on, off", self.moderator.message_history)
        self.assertIn('Vehicle spawn is [unknown]', self.moderator.message_history)

    def test_with_argument_on(self):
        self.p.console.setCvar = Mock()
        self.moderator.connects('moderator')
        self.moderator.message_history = []
        self.moderator.says('!vehicles on')
        self.assertIn('vehicle spawn is now [ON]', self.moderator.message_history)
        self.p.console.setCvar.assert_called_with('vehicleSpawnAllowed', 'true')

    def test_with_argument_off(self):
        self.p.console.setCvar = Mock()
        self.moderator.connects('moderator')
        self.moderator.message_history = []
        self.moderator.says('!vehicles off')
        self.assertIn('vehicle spawn is now [OFF]', self.moderator.message_history)
        self.p.console.setCvar.assert_called_with('vehicleSpawnAllowed', 'false')