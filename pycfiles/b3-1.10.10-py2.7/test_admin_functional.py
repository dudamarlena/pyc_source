# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: H:\workspaces\workspace-python\big-brother-bot\tests\plugins\test_admin_functional.py
# Compiled at: 2015-03-02 15:00:11
import logging, sys, os, thread, time, unittest2 as unittest
from mock import Mock
from mock import call
from mock import patch
from mock import ANY
from mockito import when
from b3 import __file__ as b3_module__file__
from b3 import TEAM_BLUE
from b3 import TEAM_RED
from b3.clients import Group
from b3.clients import Client
from tests import B3TestCase
from tests import InstantTimer
from b3.fake import FakeClient
from b3.config import CfgConfigParser
from b3.plugins.admin import AdminPlugin
ADMIN_CONFIG_FILE = os.path.join(os.path.dirname(b3_module__file__), 'conf/plugin_admin.ini')

class Admin_functional_test(B3TestCase):
    """ tests from a class inheriting from Admin_functional_test must call self.init() """

    def setUp(self):
        B3TestCase.setUp(self)
        self.conf = CfgConfigParser()
        self.p = AdminPlugin(self.console, self.conf)

    def init(self, config_content=None):
        """ optionally specify a config for the plugin. If called with no parameter, then the default config is loaded """
        if config_content is None:
            if not os.path.isfile(ADMIN_CONFIG_FILE):
                B3TestCase.tearDown(self)
                raise unittest.SkipTest('%s is not a file' % ADMIN_CONFIG_FILE)
            else:
                self.conf.load(ADMIN_CONFIG_FILE)
        else:
            self.conf.loadFromString(config_content)
        self.p._commands = {}
        self.p.onLoadConfig()
        self.p.onStartup()
        self.joe = FakeClient(self.console, name='Joe', exactName='Joe', guid='joeguid', groupBits=128, team=TEAM_RED)
        self.mike = FakeClient(self.console, name='Mike', exactName='Mike', guid='mikeguid', groupBits=1, team=TEAM_BLUE)
        return


class Cmd_baninfo(Admin_functional_test):

    def test_no_parameter(self):
        self.init()
        self.joe.connects(0)
        self.joe.says('!baninfo')
        self.assertListEqual(['Invalid parameters'], self.joe.message_history)

    def test_no_ban(self):
        self.init()
        self.joe.connects(0)
        self.mike.connects(1)
        self.joe.says('!baninfo mike')
        self.assertListEqual(['Mike has no active bans'], self.joe.message_history)

    def test_perm_ban(self):
        self.init()
        self.joe.connects(0)
        self.mike.connects(1)
        self.joe.says('!permban mike f00')
        self.joe.says('!baninfo @%s' % self.mike.id)
        self.assertListEqual(['Mike has 1 active bans'], self.joe.message_history)

    def test_temp_ban(self):
        self.init()
        self.joe.connects(0)
        self.mike.connects(1)
        self.joe.says('!ban mike f00')
        self.joe.says('!baninfo @%s' % self.mike.id)
        self.assertListEqual(['Mike has 1 active bans'], self.joe.message_history)

    def test_multiple_bans(self):
        self.init()
        self.joe.connects(0)
        self.mike.connects(1)
        self.joe.says('!ban @%s f00' % self.mike.id)
        self.joe.says('!permban @%s f00' % self.mike.id)
        self.joe.says('!baninfo @%s' % self.mike.id)
        self.assertListEqual(['Mike has 2 active bans'], self.joe.message_history)

    def test_no_ban_custom_message(self):
        self.init('\n[commands]\nbaninfo: mod\n[messages]\nbaninfo_no_bans: %(name)s is not banned\n')
        self.joe.connects(0)
        self.mike.connects(1)
        self.joe.says('!baninfo mike')
        self.assertListEqual(['Mike is not banned'], self.joe.message_history)

    def test_perm_ban_custom_message(self):
        self.init('\n[commands]\npermban: fulladmin\nbaninfo: mod\n[messages]\nbaninfo: %(name)s is banned\n')
        self.joe.connects(0)
        self.mike.connects(1)
        self.joe.says('!permban mike f00')
        self.joe.says('!baninfo @%s' % self.mike.id)
        self.assertListEqual(['Mike is banned'], self.joe.message_history)


class Cmd_putgroup(Admin_functional_test):

    def setUp(self):
        Admin_functional_test.setUp(self)
        self.init("\n[commands]\nputgroup: admin\n[messages]\ngroup_unknown: Unkonwn group: %(group_name)s\ngroup_beyond_reach: You can't assign players to group %(group_name)s\n")
        self.joe.connects(0)
        self.mike.connects(1)
        self.assertEqual('user', self.mike.maxGroup.keyword)

    def test_nominal(self):
        self.joe.clearMessageHistory()
        self.joe.says('!putgroup mike fulladmin')
        self.assertListEqual(['Mike put in group Full Admin'], self.joe.message_history)
        self.assertEqual('fulladmin', self.mike.maxGroup.keyword)

    def test_non_existing_group(self):
        self.joe.clearMessageHistory()
        self.joe.says('!putgroup mike f00')
        self.assertListEqual(['Unkonwn group: f00'], self.joe.message_history)
        self.assertEqual('user', self.mike.maxGroup.keyword)

    def test_non_existing_player(self):
        self.joe.clearMessageHistory()
        self.joe.says('!putgroup f00 admin')
        self.assertListEqual(['No players found matching f00'], self.joe.message_history)
        self.assertEqual('user', self.mike.maxGroup.keyword)

    def test_no_parameter(self):
        self.joe.clearMessageHistory()
        self.joe.says('!putgroup')
        self.assertListEqual(['Invalid parameters'], self.joe.message_history)
        self.assertEqual('user', self.mike.maxGroup.keyword)

    def test_one_parameter(self):
        self.joe.clearMessageHistory()
        self.joe.says('!putgroup mike')
        self.assertListEqual(['Invalid parameters'], self.joe.message_history)
        self.assertEqual('user', self.mike.maxGroup.keyword)

    def test_too_many_parameters(self):
        self.joe.clearMessageHistory()
        self.joe.says('!putgroup mike fulladmin 5')
        self.assertListEqual(['Invalid parameters'], self.joe.message_history)
        self.assertEqual('user', self.mike.maxGroup.keyword)

    def test_already_in_group(self):
        self.joe.clearMessageHistory()
        self.joe.says('!putgroup mike user')
        self.assertListEqual(['Mike is already in group User'], self.joe.message_history)
        self.assertEqual('user', self.mike.maxGroup.keyword)

    def test_group_beyond_reach(self):
        jack = FakeClient(self.console, name='Jack', guid='jackguid', groupBits=40, team=TEAM_RED)
        jack.connects(3)
        self.assertEqual('fulladmin', jack.maxGroup.keyword)
        jack.clearMessageHistory()
        jack.says('!putgroup mike fulladmin')
        self.assertEqual('user', self.mike.maxGroup.keyword)
        self.assertListEqual(["You can't assign players to group Full Admin"], jack.message_history)
        jack.clearMessageHistory()
        jack.says('!putgroup mike admin')
        self.assertEqual('admin', self.mike.maxGroup.keyword)
        self.assertListEqual(['Mike put in group Admin'], jack.message_history)


class Cmd_tempban(Admin_functional_test):

    def setUp(self):
        Admin_functional_test.setUp(self)
        self.init()
        self.joe.message = Mock()
        self.joe.connects(0)

    def test_no_duration(self):
        self.mike.connects(1)
        self.joe.says('!tempban mike')
        self.joe.message.assert_called_with('^7Invalid parameters')

    def test_bad_duration(self):
        self.mike.connects(1)
        self.mike.tempban = Mock()
        self.joe.says('!tempban mike 5hour')
        self.joe.message.assert_called_with('^7Invalid parameters')
        assert not self.mike.tempban.called

    def test_non_existing_player(self):
        self.mike.connects(1)
        self.joe.says('!tempban foo 5h')
        self.joe.message.assert_called_with('^7No players found matching foo')

    def test_no_reason(self):
        self.mike.connects(1)
        self.mike.tempban = Mock()
        self.joe.says('!tempban mike 5h')
        self.mike.tempban.assert_called_with('', None, 300, self.joe)
        return


class Cmd_lastbans(Admin_functional_test):

    def setUp(self):
        Admin_functional_test.setUp(self)
        self.init()
        self.joe.message = Mock()
        self.joe.connects(0)

    def test_no_ban(self):
        self.joe.says('!lastbans')
        self.joe.message.assert_called_with('^7There are no active bans')

    @patch('time.time', return_value=0)
    def test_one_tempban(self, mock_time):
        self.mike.connects(1)
        self.joe.says('!tempban mike 5h test reason')
        self.joe.says('!lastbans')
        self.joe.message.assert_called_with('^2@2^7 Mike^7^7 (5 hours remaining) test reason')
        self.joe.says('!unban @2')
        self.joe.says('!lastbans')
        self.joe.message.assert_called_with('^7There are no active bans')


class Cmd_help(Admin_functional_test):

    def setUp(self):
        Admin_functional_test.setUp(self)
        self.p._commands = {}
        self.init()
        self.joe.message = Mock()
        self.joe.connects(0)

    def test_non_existing_cmd(self):
        self.joe.says('!help fo0')
        self.joe.message.assert_called_with('^7Command not found fo0')

    def test_existing_cmd(self):
        self.joe.says('!help help')
        self.joe.message.assert_called_with('^2!help ^7%s' % self.p.cmd_help.__doc__.strip())

    def test_no_arg(self):
        self.joe.says('!help')
        self.joe.message.assert_called_with('^7Available commands: admins, admintest, aliases, b3, ban, banall, baninfo, clear, clientinfo, die, find, help, iamgod, kick, kickall, lastbans, leveltest, list, longlist, lookup, makereg, map, maprotate, maps, mask, nextmap, notice, pause, permban, poke, putgroup, rebuild, reconfig, regtest, regulars, rules, runas, say, scream, seen, spam, spams, spank, spankall, status, tempban, time, unban, ungroup, unmask, unreg, warn, warnclear, warninfo, warnremove, warns, warntest')
        self.mike.message = Mock()
        self.mike.connects(0)
        self.mike.says('!help')
        self.mike.message.assert_called_with('^7Available commands: help, iamgod, regtest, regulars, rules, time')

    def test_joker(self):
        self.joe.says('!help *ban')
        self.joe.message.assert_called_with('^7Available commands: ban, banall, baninfo, lastbans, permban, tempban, unban')


class Cmd_mask(Admin_functional_test):

    def setUp(self):
        Admin_functional_test.setUp(self)
        self.init()

    def test_nominal(self):
        self.joe.message = Mock(wraps=lambda x: sys.stdout.write('\t\t' + x + '\n'))
        self.joe.connects(0)
        self.joe.says('!admins')
        self.joe.message.assert_called_with('^7Admins online: Joe^7^7 [^3100^7]')
        self.mike.connects(1)
        self.joe.says('!putgroup mike senioradmin')
        self.joe.says('!admins')
        self.joe.message.assert_called_with('^7Admins online: Joe^7^7 [^3100^7], Mike^7^7 [^380^7]')
        self.joe.says('!mask user')
        self.joe.says('!admins')
        self.joe.message.assert_called_with('^7Admins online: Mike^7^7 [^380^7]')
        self.joe.says('!unmask')
        self.joe.says('!admins')
        self.joe.message.assert_called_with('^7Admins online: Joe^7^7 [^3100^7], Mike^7^7 [^380^7]')
        self.joe.says('!mask user mike')
        self.joe.says('!admins')
        self.joe.message.assert_called_with('^7Admins online: Joe^7^7 [^3100^7]')
        self.joe.says('!unmask mike')
        self.joe.says('!admins')
        self.joe.message.assert_called_with('^7Admins online: Joe^7^7 [^3100^7], Mike^7^7 [^380^7]')

    def _test_persistence_for_group(self, group_keyword):
        """
        Makes sure that a user with group 'superadmin', when masked as the given group is still masked with
        that given group once he reconnects. Hence making sure we persists the mask group between connections.
        :param group_keyword: str
        """
        group_to_mask_as = self.console.storage.getGroup(Group(keyword=group_keyword))
        self.assertIsNotNone(group_to_mask_as)
        self.joe.connects(0)
        self.joe.says('!mask ' + group_keyword)
        self.assertEqual(128, self.joe.maxGroup.id)
        self.assertEqual(100, self.joe.maxGroup.level)
        self.assertIsNotNone(self.joe.maskGroup, 'expecting Joe to have a masked group')
        self.assertEqual(group_to_mask_as.id, self.joe.maskGroup.id, 'expecting Joe2 to have %s for the mask group id' % group_to_mask_as.id)
        self.assertEqual(group_to_mask_as.level, self.joe.maskGroup.level, 'expecting Joe2 to have %s for the mask group level' % group_to_mask_as.level)
        self.assertEqual(group_to_mask_as.id, self.joe.maskedGroup.id, 'expecting Joe2 to have %s for the masked group id' % group_to_mask_as.id)
        self.assertEqual(group_to_mask_as.level, self.joe.maskedGroup.level, 'expecting Joe2 to have %s for the masked group level' % group_to_mask_as.level)
        self.joe.disconnects()
        client = self.console.storage.getClient(Client(id=self.joe.id))
        joe2 = FakeClient(self.console, **client.__dict__)
        joe2.connects(1)
        self.assertEqual(128, joe2.maxGroup.id)
        self.assertEqual(100, joe2.maxGroup.level)
        self.assertIsNotNone(joe2.maskGroup, 'expecting Joe2 to have a masked group')
        self.assertEqual(group_to_mask_as.id, joe2.maskGroup.id, 'expecting Joe2 to have %s for the mask group id' % group_to_mask_as.id)
        self.assertEqual(group_to_mask_as.level, joe2.maskGroup.level, 'expecting Joe2 to have %s for the mask group level' % group_to_mask_as.level)
        self.assertEqual(group_to_mask_as.id, joe2.maskedGroup.id, 'expecting Joe2 to have %s for the masked group id' % group_to_mask_as.id)
        self.assertEqual(group_to_mask_as.level, joe2.maskedGroup.level, 'expecting Joe2 to have %s for the masked group level' % group_to_mask_as.level)
        client_data = self.console.storage.getClient(Client(id=joe2.id))
        self.assertIsNotNone(client_data)
        self.assertEqual(group_to_mask_as.level, client_data._maskLevel, 'expecting %s to be the value in the mask_level column in database' % group_to_mask_as.level)

    def test_persistence(self):
        self._test_persistence_for_group('user')
        self._test_persistence_for_group('reg')
        self._test_persistence_for_group('mod')
        self._test_persistence_for_group('admin')
        self._test_persistence_for_group('fulladmin')
        self._test_persistence_for_group('senioradmin')
        self._test_persistence_for_group('superadmin')


class Cmd_makereg_unreg(Admin_functional_test):

    def setUp(self):
        Admin_functional_test.setUp(self)
        self.init()
        self.group_user = self.console.storage.getGroup(Group(keyword='user'))
        self.group_reg = self.console.storage.getGroup(Group(keyword='reg'))
        self.joe.message = Mock(wraps=lambda x: sys.stdout.write('\t\t' + x + '\n'))
        self.joe.connects(0)
        self.mike.connects(1)

    def test_nominal(self):
        self.assertTrue(self.mike.inGroup(self.group_user))
        self.assertFalse(self.mike.inGroup(self.group_reg))
        self.joe.says('!makereg mike')
        self.assertFalse(self.mike.inGroup(self.group_user))
        self.assertTrue(self.mike.inGroup(self.group_reg))
        self.joe.message.assert_called_with('^7Mike^7 ^7put in group Regular')
        self.joe.says('!unreg mike')
        self.assertTrue(self.mike.inGroup(self.group_user))
        self.assertFalse(self.mike.inGroup(self.group_reg))
        self.joe.message.assert_called_with('^7Mike^7^7 removed from group Regular')

    def test_unreg_when_not_regular(self):
        self.assertTrue(self.mike.inGroup(self.group_user))
        self.assertFalse(self.mike.inGroup(self.group_reg))
        self.joe.says('!unreg mike')
        self.assertTrue(self.mike.inGroup(self.group_user))
        self.assertFalse(self.mike.inGroup(self.group_reg))
        self.joe.message.assert_called_with('^7Mike^7^7 is not in group Regular')

    def test_makereg_when_already_regular(self):
        self.mike.addGroup(self.group_reg)
        self.mike.remGroup(self.group_user)
        self.assertTrue(self.mike.inGroup(self.group_reg))
        self.joe.says('!makereg mike')
        self.assertFalse(self.mike.inGroup(self.group_user))
        self.assertTrue(self.mike.inGroup(self.group_reg))
        self.joe.message.assert_called_with('^7Mike^7^7 is already in group Regular')

    def test_makereg_no_parameter(self):
        self.joe.says('!makereg')
        self.joe.message.assert_called_with('^7Invalid parameters')

    def test_unreg_no_parameter(self):
        self.joe.says('!unreg')
        self.joe.message.assert_called_with('^7Invalid parameters')

    def test_makereg_unknown_player(self):
        self.joe.says('!makereg foo')
        self.joe.message.assert_called_with('^7No players found matching foo')

    def test_unreg_unknown_player(self):
        self.joe.says('!unreg foo')
        self.joe.message.assert_called_with('^7No players found matching foo')


def _start_new_thread(callable, args_list, kwargs_dict):
    """ used to patch thread.start_new_thread so it won't create a new thread but call the callable synchronously """
    callable(*args_list, **kwargs_dict)


@patch.object(time, 'sleep')
@patch.object(thread, 'start_new_thread', wraps=_start_new_thread)
class Cmd_rules(Admin_functional_test):

    def setUp(self):
        Admin_functional_test.setUp(self)
        self.init()

    def test_nominal(self, start_new_thread_mock, sleep_mock):
        self.joe.message = Mock(wraps=lambda x: sys.stdout.write('\t\t' + x + '\n'))
        self.joe.connects(0)
        self.joe.says('!rules')
        self.joe.message.assert_has_calls([call('^3Rule #1: No racism of any kind'),
         call('^3Rule #2: No clan stacking, members must split evenly between the teams'),
         call('^3Rule #3: No arguing with admins (listen and learn or leave)'),
         call('^3Rule #4: No abusive language or behavior towards admins or other players'),
         call('^3Rule #5: No offensive or potentially offensive names, annoying names, or in-game (double caret (^)) color in names'),
         call('^3Rule #6: No recruiting for your clan, your server, or anything else'),
         call('^3Rule #7: No advertising or spamming of websites or servers'),
         call('^3Rule #8: No profanity or offensive language (in any language)'),
         call('^3Rule #9: Do ^1NOT ^3fire at teammates or within 10 seconds of spawning'),
         call('^3Rule #10: Offense players must play for the objective and support their team')])

    def test_nominal_loud(self, start_new_thread_mock, sleep_mock):
        self.console.say = Mock(wraps=lambda x: sys.stdout.write('\t\t' + x + '\n'))
        self.joe.connects(0)
        self.joe.says('@rules')
        self.console.say.assert_has_calls([call('^3Rule #1: No racism of any kind'),
         call('^3Rule #2: No clan stacking, members must split evenly between the teams'),
         call('^3Rule #3: No arguing with admins (listen and learn or leave)'),
         call('^3Rule #4: No abusive language or behavior towards admins or other players'),
         call('^3Rule #5: No offensive or potentially offensive names, annoying names, or in-game (double caret (^)) color in names'),
         call('^3Rule #6: No recruiting for your clan, your server, or anything else'),
         call('^3Rule #7: No advertising or spamming of websites or servers'),
         call('^3Rule #8: No profanity or offensive language (in any language)'),
         call('^3Rule #9: Do ^1NOT ^3fire at teammates or within 10 seconds of spawning'),
         call('^3Rule #10: Offense players must play for the objective and support their team')])

    def test_nominal_bigtext(self, start_new_thread_mock, sleep_mock):
        self.console.saybig = Mock(wraps=lambda x: sys.stdout.write('\t\t' + x + '\n'))
        self.joe.connects(0)
        self.joe.says('&rules')
        self.console.saybig.assert_has_calls([call('^3Rule #1: No racism of any kind'),
         call('^3Rule #2: No clan stacking, members must split evenly between the teams'),
         call('^3Rule #3: No arguing with admins (listen and learn or leave)'),
         call('^3Rule #4: No abusive language or behavior towards admins or other players'),
         call('^3Rule #5: No offensive or potentially offensive names, annoying names, or in-game (double caret (^)) color in names'),
         call('^3Rule #6: No recruiting for your clan, your server, or anything else'),
         call('^3Rule #7: No advertising or spamming of websites or servers'),
         call('^3Rule #8: No profanity or offensive language (in any language)'),
         call('^3Rule #9: Do ^1NOT ^3fire at teammates or within 10 seconds of spawning'),
         call('^3Rule #10: Offense players must play for the objective and support their team')])

    def test_nominal_to_player(self, start_new_thread_mock, sleep_mock):
        self.joe.message = Mock(wraps=lambda x: sys.stdout.write('\t\t' + x + '\n'))
        self.joe.connects(0)
        self.mike.message = Mock(wraps=lambda x: sys.stdout.write('\t\t' + x + '\n'))
        self.mike.connects(1)
        self.joe.says('!rules mike')
        self.mike.message.assert_has_calls([call('^3Rule #1: No racism of any kind'),
         call('^3Rule #2: No clan stacking, members must split evenly between the teams'),
         call('^3Rule #3: No arguing with admins (listen and learn or leave)'),
         call('^3Rule #4: No abusive language or behavior towards admins or other players'),
         call('^3Rule #5: No offensive or potentially offensive names, annoying names, or in-game (double caret (^)) color in names'),
         call('^3Rule #6: No recruiting for your clan, your server, or anything else'),
         call('^3Rule #7: No advertising or spamming of websites or servers'),
         call('^3Rule #8: No profanity or offensive language (in any language)'),
         call('^3Rule #9: Do ^1NOT ^3fire at teammates or within 10 seconds of spawning'),
         call('^3Rule #10: Offense players must play for the objective and support their team')])

    def test_unknown_player(self, start_new_thread_mock, sleep_mock):
        self.joe.message = Mock(wraps=lambda x: sys.stdout.write('\t\t' + x + '\n'))
        self.joe.connects(0)
        self.joe.says('!rules fOO')
        self.joe.message.assert_has_calls([call('^7No players found matching fOO')])


class Cmd_warns(Admin_functional_test):

    def setUp(self):
        Admin_functional_test.setUp(self)
        self.init()

    def test_nominal(self):
        self.joe.message = Mock(wraps=lambda x: sys.stdout.write('\t\t' + x + '\n'))
        self.joe.connects(0)
        self.joe.says('!warns')
        self.joe.message.assert_called_once_with('^7Warnings: adv, afk, argue, badname, camp, ci, color, cuss, fakecmd, jerk, lang, language, name, nocmd, obj, profanity, racism, recruit, rule1, rule10, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, sfire, spam, spawnfire, spec, spectator, stack, tk')


class Test_warn_reasons_default_config(Admin_functional_test):

    def setUp(self):
        Admin_functional_test.setUp(self)
        self.init()
        self.joe.connects(0)
        self.mike.connects(1)

    def test_no_reason(self):
        with patch.object(self.mike, 'warn') as (mock):
            self.joe.says('!warn mike')
            mock.assert_has_calls([call(60.0, '^7behave yourself', None, self.joe, '')])
        return

    def test_reason_is_not_a_keyword(self):
        with patch.object(self.mike, 'warn') as (mock):
            self.joe.says('!warn mike f00')
            mock.assert_has_calls([call(60.0, '^7 f00', 'f00', self.joe, '')])

    def test_reason_is_a_keyword(self):
        with patch.object(self.mike, 'warn') as (warn_mock):

            def assertWarn(keyword, duration, text):
                warn_mock.reset_mock()
                self.mike.delvar(self.p, 'warnTime')
                self.joe.says('!warn mike %s' % keyword)
                warn_mock.assert_has_calls([call(float(duration), text, keyword, self.joe, '')])

            assertWarn('rule1', 14400, '^3Rule #1: No racism of any kind')
            assertWarn('rule2', 1440, '^3Rule #2: No clan stacking, members must split evenly between the teams')
            assertWarn('rule3', 1440, '^3Rule #3: No arguing with admins (listen and learn or leave)')
            assertWarn('rule4', 1440, '^3Rule #4: No abusive language or behavior towards admins or other players')
            assertWarn('rule5', 60, '^3Rule #5: No offensive or potentially offensive names, annoying names, or in-game (double caret (^)) color in names')
            assertWarn('rule6', 1440, '^3Rule #6: No recruiting for your clan, your server, or anything else')
            assertWarn('rule7', 1440, '^3Rule #7: No advertising or spamming of websites or servers')
            assertWarn('rule8', 4320, '^3Rule #8: No profanity or offensive language (in any language)')
            assertWarn('rule9', 180, '^3Rule #9: Do ^1NOT ^3fire at teammates or within 10 seconds of spawning')
            assertWarn('rule10', 4320, '^3Rule #10: Offense players must play for the objective and support their team')
            assertWarn('stack', 1440, '^3Rule #2: No clan stacking, members must split evenly between the teams')
            assertWarn('lang', 4320, '^3Rule #8: No profanity or offensive language (in any language)')
            assertWarn('language', 4320, '^3Rule #8: No profanity or offensive language (in any language)')
            assertWarn('cuss', 4320, '^3Rule #8: No profanity or offensive language (in any language)')
            assertWarn('profanity', 4320, '^3Rule #8: No profanity or offensive language (in any language)')
            assertWarn('name', 60, '^3Rule #5: No offensive or potentially offensive names, annoying names, or in-game (double caret (^)) color in names')
            assertWarn('color', 60, '^7No in-game (double caret (^)) color in names')
            assertWarn('badname', 60, '^7No offensive, potentially offensive, or annoying names')
            assertWarn('spec', 5, '^7spectator too long on full server')
            assertWarn('adv', 1440, '^3Rule #7: No advertising or spamming of websites or servers')
            assertWarn('racism', 14400, '^3Rule #1: No racism of any kind')
            assertWarn('stack', 1440, '^3Rule #2: No clan stacking, members must split evenly between the teams')
            assertWarn('recruit', 1440, '^3Rule #6: No recruiting for your clan, your server, or anything else')
            assertWarn('argue', 1440, '^3Rule #3: No arguing with admins (listen and learn or leave)')
            assertWarn('sfire', 180, '^3Rule #9: Do ^1NOT ^3fire at teammates or within 10 seconds of spawning')
            assertWarn('spawnfire', 180, '^3Rule #9: Do ^1NOT ^3fire at teammates or within 10 seconds of spawning')
            assertWarn('jerk', 1440, '^3Rule #4: No abusive language or behavior towards admins or other players')
            assertWarn('afk', 5, '^7you appear to be away from your keyboard')
            assertWarn('tk', 1440, '^7stop team killing!')
            assertWarn('obj', 60, '^7go for the objective!')
            assertWarn('camp', 60, '^7stop camping or you will be kicked!')
            assertWarn('fakecmd', 60, '^7do not use fake commands')
            assertWarn('nocmd', 60, '^7do not use commands that you do not have access to, try using !help')
            assertWarn('ci', 5, '^7connection interupted, reconnect')
            assertWarn('spectator', 5, '^7spectator too long on full server')
            assertWarn('spam', 60, '^7do not spam, shut-up!')


class Test_reason_keywords(Admin_functional_test):

    def setUp(self):
        Admin_functional_test.setUp(self)
        self.init()
        self.joe.connects(0)
        self.mike.connects(1)
        self.adv_text = '^3Rule #7: No advertising or spamming of websites or servers'

    def test_warn_with_keyword(self):
        with patch.object(self.console, 'say') as (say_mock):
            self.joe.says('!warn mike adv')
            say_mock.assert_has_calls([call('^1WARNING^7 [^31^7]: Mike^7^7, %s' % self.adv_text)])

    def test_warn_with_unknown_keyword(self):
        with patch.object(self.console, 'say') as (say_mock):
            self.joe.says('!warn mike f00')
            say_mock.assert_has_calls([call('^1WARNING^7 [^31^7]: Mike^7^7, ^7 f00')])

    def test_notice_with_keyword(self):
        with patch.object(self.mike, 'notice') as (notice_mock):
            self.joe.says('!notice mike adv')
            notice_mock.assert_has_calls([call('adv', None, self.joe)])
        return

    def test_notice_with_unknown_keyword(self):
        with patch.object(self.mike, 'notice') as (notice_mock):
            self.joe.says('!notice mike f00')
            notice_mock.assert_has_calls([call('f00', None, self.joe)])
        return

    def test_kick_with_keyword(self):
        with patch.object(self.console, 'kick') as (kick_mock):
            self.joe.says('!kick mike adv')
            kick_mock.assert_has_calls([call(self.mike, self.adv_text, self.joe, False)])

    def test_kick_with_unknown_keyword(self):
        with patch.object(self.console, 'kick') as (kick_mock):
            self.joe.says('!kick mike f00')
            kick_mock.assert_has_calls([call(self.mike, 'f00', self.joe, False)])

    def test_ban_with_keyword(self):
        with patch.object(self.mike, 'tempban') as (tempban_mock):
            self.joe.says('!ban mike adv')
            tempban_mock.assert_has_calls([call(self.adv_text, 'adv', 20160.0, self.joe)])

    def test_ban_with_unknown_keyword(self):
        with patch.object(self.mike, 'tempban') as (tempban_mock):
            self.joe.says('!ban mike f00')
            tempban_mock.assert_has_calls([call('f00', 'f00', 20160.0, self.joe)])

    def test_permban_with_keyword(self):
        with patch.object(self.mike, 'ban') as (permban_mock):
            self.joe.says('!permban mike adv')
            permban_mock.assert_has_calls([call(self.adv_text, 'adv', self.joe)])

    def test_permban_with_unknown_keyword(self):
        with patch.object(self.mike, 'ban') as (permban_mock):
            self.joe.says('!permban mike f00')
            permban_mock.assert_has_calls([call('f00', 'f00', self.joe)])


@unittest.skipUnless(os.path.isfile(ADMIN_CONFIG_FILE), '%s is not a file' % ADMIN_CONFIG_FILE)
class Test_config(Admin_functional_test):

    def setUp(self):
        Admin_functional_test.setUp(self)
        logging.getLogger('output').setLevel(logging.INFO)

    def test_no_generic_or_default_warn_reason(self):
        new_config_content = ''
        with open(ADMIN_CONFIG_FILE) as (config_file):
            is_in_warn_reasons_section = False
            for line in config_file:
                if line == '[warn_reasons]':
                    is_in_warn_reasons_section = True
                if not is_in_warn_reasons_section:
                    new_config_content += line + '\n'
                elif line.startswith('['):
                    new_config_content += line + '\n'
                    is_in_warn_reasons_section = False
                elif line.startswith('generic') or line.startswith('default'):
                    pass
                else:
                    new_config_content += line + '\n'

        self.init(new_config_content)
        self.joe.message = Mock(lambda x: sys.stdout.write('message to Joe: ' + x + '\n'))
        self.joe.connects(0)
        self.joe.says('!warntest')
        self.joe.message.assert_called_once_with('^2TEST: ^1WARNING^7 [^31^7]: ^7behave yourself')
        self.joe.message.reset_mock()
        self.joe.says('!warntest argue')
        self.joe.message.assert_called_once_with('^2TEST: ^1WARNING^7 [^31^7]: ^3Rule #3: No arguing with admins (listen and learn or leave)')

    def test_bad_format_for_generic_and_default(self):
        self.init('[warn_reasons]\ngeneric: 1h\ndefault: /\n')
        self.assertEqual((60, '^7'), self.p.warn_reasons['generic'])
        self.assertEqual((60, '^7behave yourself'), self.p.warn_reasons['default'])

    def test_bad_format_1(self):
        self.init('[warn_reasons]\nfoo: foo\nbar: 5d\n')
        self.assertNotIn('foo', self.p.warn_reasons)

    def test_bad_format_2(self):
        self.init('[warn_reasons]\nfoo: /foo bar\n')
        self.assertNotIn('foo', self.p.warn_reasons)

    def test_bad_format_3(self):
        self.init('[warn_reasons]\nfoo: /spam#\nbar: /spam# qsdf sq\n')
        self.assertNotIn('foo', self.p.warn_reasons)

    def test_reference_to_warn_reason(self):
        self.init('[warn_reasons]\nfoo: 2h, foo\nbar: /foo\n')
        self.assertIn('foo', self.p.warn_reasons)
        self.assertEqual((120, 'foo'), self.p.warn_reasons['foo'])
        self.assertIn('bar', self.p.warn_reasons)
        self.assertEqual((120, 'foo'), self.p.warn_reasons['bar'])

    def test_invalid_reference_to_warn_reason(self):
        self.init('[warn_reasons]\nfoo: 2h, foo\nbar: /nonexisting\n')
        self.assertIn('foo', self.p.warn_reasons)
        self.assertEqual((120, 'foo'), self.p.warn_reasons['foo'])
        self.assertNotIn('bar', self.p.warn_reasons)

    def test_reference_to_spamage(self):
        self.init('[spamages]\nfoo: fOO fOO\n[warn_reasons]\nbar: 4h, /spam#foo\n')
        self.assertIn('bar', self.p.warn_reasons)
        self.assertEqual((240, 'fOO fOO'), self.p.warn_reasons['bar'])

    def test_invalid_reference_to_spamage(self):
        self.init('[warn_reasons]\nbar: 4h, /spam#foo\n')
        self.assertNotIn('bar', self.p.warn_reasons)


class Cmd_admins(Admin_functional_test):

    def test_no_admin(self):
        self.init('\n[commands]\nadmins: user\n')
        self.mike.connects(0)
        self.mike.clearMessageHistory()
        self.mike.says('!admins')
        self.assertListEqual(['There are no admins online'], self.mike.message_history)

    def test_no_admin_custom_message(self):
        self.init('\n[commands]\nadmins: user\n[messages]\nno_admins: no admins\n')
        self.mike.connects(0)
        self.mike.clearMessageHistory()
        self.mike.says('!admins')
        self.assertListEqual(['no admins'], self.mike.message_history)

    def test_no_admin_blank_message(self):
        self.init('\n[commands]\nadmins: user\n[messages]\nno_admins:\n')
        self.mike.connects(0)
        self.mike.clearMessageHistory()
        self.mike.says('!admins')
        self.assertListEqual([], self.mike.message_history)

    def test_one_admin(self):
        self.init()
        self.joe.connects(0)
        self.joe.clearMessageHistory()
        self.joe.says('!admins')
        self.assertListEqual(['Admins online: Joe [100]'], self.joe.message_history)

    def test_one_admin_custom_message(self):
        self.init('\n[commands]\nadmins: mod\n[messages]\nadmins: online admins: %s\n')
        self.joe.connects(0)
        self.joe.clearMessageHistory()
        self.joe.says('!admins')
        self.assertListEqual(['online admins: Joe [100]'], self.joe.message_history)

    def test_two_admins(self):
        self.init()
        self.joe.connects(0)
        self.mike.connects(1)
        self.joe.says('!putgroup mike senioradmin')
        self.joe.clearMessageHistory()
        self.joe.says('!admins')
        self.assertListEqual(['Admins online: Joe [100], Mike [80]'], self.joe.message_history)


class Cmd_regulars(Admin_functional_test):

    def setUp(self):
        Admin_functional_test.setUp(self)
        self.init()
        self.joe.message = Mock(wraps=lambda x: sys.stdout.write('\t\t' + x + '\n'))
        self.joe.connects(0)

    def test_no_regular(self):
        self.joe.says('!regulars')
        self.joe.message.assert_called_with('^7There are no regular players online')

    def test_one_regular(self):
        self.mike.connects(1)
        self.joe.says('!makereg mike')
        self.joe.says('!regs')
        self.joe.message.assert_called_with('^7Regular players online: Mike^7')

    def test_two_regulars(self):
        self.mike.connects(1)
        self.joe.says('!makereg mike')
        self.jack = FakeClient(self.console, name='Jack', guid='jackguid', groupBits=1)
        self.jack.connects(2)
        self.joe.says('!makereg jack')
        self.joe.says('!regs')
        self.joe.message.assert_called_with('^7Regular players online: Mike^7, Jack^7')


class Cmd_map(Admin_functional_test):

    def setUp(self):
        Admin_functional_test.setUp(self)
        self.init()

    def test_missing_param(self):
        self.joe.message = Mock(wraps=lambda x: sys.stdout.write('\t\t' + x + '\n'))
        self.joe.connects(0)
        self.joe.says('!map')
        self.joe.message.assert_called_once_with('^7You must supply a map to change to')

    def test_suggestions(self):
        self.joe.message = Mock(wraps=lambda x: sys.stdout.write('\t\t' + x + '\n'))
        self.joe.connects(0)
        when(self.console).changeMap('f00').thenReturn(['bar1', 'bar2', 'bar3', 'bar4', 'bar5', 'bar6', 'bar7', 'bar8', 'bar9', 'bar10', 'bar11', 'bar'])
        self.joe.says('!map f00')
        self.joe.message.assert_called_once_with('do you mean: bar1, bar2, bar3, bar4, bar5?')

    def test_nominal(self):
        self.joe.message = Mock(wraps=lambda x: sys.stdout.write('\t\t' + x + '\n'))
        self.joe.connects(0)
        when(self.console).changeMap('f00').thenReturn(None)
        self.joe.says('!map f00')
        self.assertEqual(0, self.joe.message.call_count)
        return


class spell_checker(Admin_functional_test):

    def setUp(self):
        Admin_functional_test.setUp(self)
        self.init()
        self.joe.connects(0)

    def test_existing_command(self):
        self.joe.says('!map')
        self.assertEqual(['You must supply a map to change to'], self.joe.message_history)

    def test_misspelled_command(self):
        self.joe.says('!mip')
        self.assertEqual(['Unrecognized command mip. Did you mean !map?'], self.joe.message_history)

    def test_unrecognized_command(self):
        self.joe.says('!qfsmlkjazemlrkjazemrlkj')
        self.assertEqual(['Unrecognized command qfsmlkjazemlrkjazemrlkj'], self.joe.message_history)

    def test_existing_command_loud(self):
        self.joe.says('@map')
        self.assertEqual(['You must supply a map to change to'], self.joe.message_history)

    def test_misspelled_command_loud(self):
        self.joe.says('@mip')
        self.assertEqual(['Unrecognized command mip. Did you mean @map?'], self.joe.message_history)

    def test_unrecognized_command_loud(self):
        self.joe.says('@qfsmlkjazemlrkjazemrlkj')
        self.assertEqual(['Unrecognized command qfsmlkjazemlrkjazemrlkj'], self.joe.message_history)

    def test_existing_command_private(self):
        self.joe.says('/map')
        self.assertEqual(['You must supply a map to change to'], self.joe.message_history)

    def test_misspelled_command_private(self):
        self.joe.says('/mip')
        self.assertEqual(['Unrecognized command mip. Did you mean /map?'], self.joe.message_history)

    def test_unrecognized_command_private(self):
        self.joe.says('/qfsmlkjazemlrkjazemrlkj')
        self.assertEqual(['Unrecognized command qfsmlkjazemlrkjazemrlkj'], self.joe.message_history)


class Cmd_register(Admin_functional_test):

    def setUp(self):
        Admin_functional_test.setUp(self)
        self.p._commands = {}
        self.say_patcher = patch.object(self.console, 'say')
        self.say_mock = self.say_patcher.start()
        self.player = FakeClient(self.console, name='TestPlayer', guid='player_guid', groupBits=0)
        self.player.connects('0')

    def tearDown(self):
        Admin_functional_test.tearDown(self)
        self.say_patcher.stop()

    def test_nominal_with_defaults(self):
        self.init('\n[commands]\nregister: guest\n[messages]\nregme_annouce: %s put in group %s\n')
        self.player.says('!register')
        self.assertListEqual(['Thanks for your registration. You are now a member of the group User'], self.player.message_history)
        self.assertListEqual([call('TestPlayer^7 put in group User')], self.say_mock.mock_calls)

    def test_custom_messages(self):
        self.init('\n[commands]\nregister: guest\n[settings]\nannounce_registration: yes\n[messages]\nregme_confirmation: You are now a member of the group %s\nregme_annouce: %s is now a member of group %s\n')
        self.player.says('!register')
        self.assertListEqual(['You are now a member of the group User'], self.player.message_history)
        self.assertListEqual([call('TestPlayer^7 is now a member of group User')], self.say_mock.mock_calls)

    def test_no_announce(self):
        self.init('\n[commands]\nregister: guest\n[settings]\nannounce_registration: no\n[messages]\nregme_confirmation: You are now a member of the group %s\nregme_annouce: %s is now a member of group %s\n')
        self.player.says('!register')
        self.assertListEqual(['You are now a member of the group User'], self.player.message_history)
        self.assertListEqual([], self.say_mock.mock_calls)


@patch('time.sleep')
class Cmd_spams(Admin_functional_test):

    def test_nominal(self, sleep_mock):
        self.init('\n[commands]\nspams: 20\n[spamages]\nfoo: foo\nrule1: this is rule #1\nrule2: this is rule #2\nbar: bar\n')
        self.joe.connects(0)
        self.joe.says('!spams')
        self.assertListEqual(['Spamages: bar, foo, rule1, rule2'], self.joe.message_history)

    def test_no_spamage(self, sleep_mock):
        self.init('\n[commands]\nspams: 20\n[spamages]\n')
        self.joe.connects(0)
        self.joe.says('!spams')
        self.assertListEqual(['No spamage message defined'], self.joe.message_history)

    def test_reconfig_loads_new_spamages(self, sleep_mock):
        first_config = '\n[commands]\nspams: 20\n[spamages]\nfoo: foo\nrule1: this is rule #1\n'
        second_config = '\n[commands]\nspams: 20\n[spamages]\nbar: bar\nrule2: this is rule #2\n'
        self.init(first_config)
        self.joe.connects(0)
        self.joe.says('!spams')
        self.assertListEqual(['Spamages: foo, rule1'], self.joe.message_history)
        self.p.config = CfgConfigParser()
        self.p.config.loadFromString(second_config)
        self.joe.clearMessageHistory()
        self.joe.says('!spams')
        self.assertListEqual(['Spamages: bar, rule2'], self.joe.message_history)


@patch('time.sleep')
class Cmd_warn_and_clear(Admin_functional_test):

    def setUp(self):
        Admin_functional_test.setUp(self)
        self.init("\n[commands]\nwarn: user\nclear: user\n[messages]\nwarn_too_fast: Only one warning every %(num_second)s seconds can be given\nwarn_self: %s, you cannot give yourself a warning\nwarn_denied: %s, %s is a higher level admin, you can't warn him\ncleared_warnings: %(admin)s has cleared %(player)s of all warnings\ncleared_warnings_for_all: %(admin)s has cleared everyone's warnings and tk points\n[warn]\ntempban_num: 3\nduration_divider: 30\nmax_duration: 1d\nalert: ^1ALERT^7: $name^7 auto-kick from warnings if not cleared [^3$warnings^7] $reason\nalert_kick_num: 3\nreason: ^7too many warnings: $reason\nmessage: ^1WARNING^7 [^3$warnings^7]: $reason\n")
        self.joe.connects(0)
        self.mike.connects(1)
        self.say_patcher = patch.object(self.console, 'say')
        self.say_mock = self.say_patcher.start()
        self.mike_warn_patcher = patch.object(self.mike, 'warn', wraps=self.mike.warn)
        self.mike_warn_mock = self.mike_warn_patcher.start()

    def tearDown(self):
        Admin_functional_test.tearDown(self)
        self.say_patcher.stop()
        self.mike_warn_patcher.stop()

    def test_warn(self, sleep_mock):
        self.joe.says('!warn mike')
        self.assertEqual(1, self.mike.numWarnings)
        self.assertListEqual([call(60.0, '^7behave yourself', None, self.joe, '')], self.mike_warn_mock.mock_calls)
        self.assertListEqual([call('^1WARNING^7 [^31^7]: Mike^7^7, ^7behave yourself')], self.say_mock.mock_calls)
        self.assertListEqual([], self.joe.message_history)
        self.assertListEqual([], self.mike.message_history)
        return

    @patch('threading.Timer', new_callable=lambda : InstantTimer)
    def test_warn_then_auto_kick(self, instant_timer, sleep_mock):
        self.p.warn_delay = 0
        self.assertEqual(0, self.mike.numWarnings)
        with patch.object(self.mike, 'tempban') as (mike_tempban_mock):
            self.joe.says('!warn mike')
            self.joe.says('!warn mike')
            self.joe.says('!warn mike')
        self.assertEqual(3, self.mike.numWarnings)
        self.assertListEqual([
         call('^1WARNING^7 [^31^7]: Mike^7^7, ^7behave yourself'),
         call('^1WARNING^7 [^32^7]: Mike^7^7, ^7behave yourself'),
         call('^1WARNING^7 [^33^7]: Mike^7^7, ^7behave yourself'),
         call('^1ALERT^7: Mike^7^7 auto-kick from warnings if not cleared [^33^7] ^7behave yourself')], self.say_mock.mock_calls)
        self.assertListEqual([
         call('^7too many warnings: ^7behave yourself', 'None', 6, self.joe, False, '')], mike_tempban_mock.mock_calls)
        self.assertListEqual([], self.joe.message_history)
        self.assertListEqual([], self.mike.message_history)

    @patch('threading.Timer', new_callable=lambda : InstantTimer)
    def test_warn_then_auto_kick_duration_divider_60(self, instant_timer, sleep_mock):
        self.p.config._sections['warn']['duration_divider'] = '60'
        self.p.warn_delay = 0
        self.assertEqual(0, self.mike.numWarnings)
        with patch.object(self.mike, 'tempban') as (mike_tempban_mock):
            self.joe.says('!warn mike')
            self.joe.says('!warn mike')
            self.joe.says('!warn mike')
        self.assertEqual(3, self.mike.numWarnings)
        self.assertListEqual([
         call('^1WARNING^7 [^31^7]: Mike^7^7, ^7behave yourself'),
         call('^1WARNING^7 [^32^7]: Mike^7^7, ^7behave yourself'),
         call('^1WARNING^7 [^33^7]: Mike^7^7, ^7behave yourself'),
         call('^1ALERT^7: Mike^7^7 auto-kick from warnings if not cleared [^33^7] ^7behave yourself')], self.say_mock.mock_calls)
        self.assertListEqual([
         call('^7too many warnings: ^7behave yourself', 'None', 3, self.joe, False, '')], mike_tempban_mock.mock_calls)
        self.assertListEqual([], self.joe.message_history)
        self.assertListEqual([], self.mike.message_history)

    def test_warn_self(self, sleep_mock):
        self.joe.says('!warn joe')
        self.assertEqual(0, self.joe.numWarnings)
        self.assertListEqual(['Joe, you cannot give yourself a warning'], self.joe.message_history)

    def test_warn_denied(self, sleep_mock):
        self.mike.says('!warn joe')
        self.assertEqual(0, self.joe.numWarnings)
        self.assertListEqual(["Mike, Joe is a higher level admin, you can't warn him"], self.mike.message_history)

    def test_clear_player(self, sleep_mock):
        self.joe.says('!warn mike')
        self.assertEqual(1, self.mike.numWarnings)
        self.joe.says('!clear mike')
        self.assertListEqual([call('^1WARNING^7 [^31^7]: Mike^7^7, ^7behave yourself'),
         call('Joe^7 has cleared Mike^7 of all warnings')], self.say_mock.mock_calls)
        self.assertEqual(0, self.mike.numWarnings)

    def test_clear__all_players(self, sleep_mock):
        self.joe.says('!warn mike')
        self.assertEqual(1, self.mike.numWarnings)
        self.joe.says('!clear')
        self.assertListEqual([call('^1WARNING^7 [^31^7]: Mike^7^7, ^7behave yourself'),
         call("Joe^7 has cleared everyone's warnings and tk points")], self.say_mock.mock_calls)
        self.assertEqual(0, self.mike.numWarnings)


@patch('time.sleep')
class Test_warn_command_abusers(Admin_functional_test):

    def setUp(self):
        Admin_functional_test.setUp(self)
        self.player = FakeClient(self.console, name='ThePlayer', guid='theplayerguid', groupBits=0)
        self.player_warn_patcher = patch.object(self.player, 'warn')
        self.player_warn_mock = self.player_warn_patcher.start()

    def tearDown(self):
        Admin_functional_test.tearDown(self)
        self.player_warn_patcher.stop()

    def test_conf_empty(self, sleep_mock):
        self.init('\n[commands]\n[warn]\n')
        self.assertFalse(self.p._warn_command_abusers)
        self.assertIsNone(self.p.getWarning('fakecmd'))
        self.assertIsNone(self.p.getWarning('nocmd'))

    def test_warn_reasons(self, sleep_mock):
        self.init('\n[warn_reasons]\nfakecmd: 1h, ^7do not use fake commands\nnocmd: 1h, ^7do not use commands that you do not have access to, try using !help\n')
        self.assertTupleEqual((60.0, '^7do not use commands that you do not have access to, try using !help'), self.p.getWarning('nocmd'))
        self.assertTupleEqual((60.0, '^7do not use fake commands'), self.p.getWarning('fakecmd'))

    def test_warn_no__no_sufficient_access(self, sleep_mock):
        self.init('\n[commands]\nhelp: 2\n[warn]\nwarn_command_abusers: no\n')
        self.assertFalse(self.p._warn_command_abusers)
        self.player.connects('0')
        with patch.object(self.p, 'info') as (info_mock):
            self.player.says('!help')
        self.assertListEqual([call('ThePlayer does not have sufficient rights to use !help. Required level: 2')], info_mock.mock_calls)
        self.assertListEqual(['You do not have sufficient access to use !help'], self.player.message_history)
        self.assertFalse(self.player_warn_mock.called)

    def test_warn_yes__no_sufficient_access(self, sleep_mock):
        self.init('\n[commands]\nhelp: 2\n[warn]\nwarn_command_abusers: yes\n')
        self.assertTrue(self.p._warn_command_abusers)
        self.player.connects('0')
        with patch.object(self.p, 'info') as (info_mock):
            self.player.says('!help')
        self.assertListEqual([call('ThePlayer does not have sufficient rights to use !help. Required level: 2')], info_mock.mock_calls)
        self.assertListEqual(['You do not have sufficient access to use !help'], self.player.message_history)
        self.assertFalse(self.player_warn_mock.called)

    def test_warn_yes__no_sufficient_access_abuser(self, sleep_mock):
        self.init('\n[commands]\nhelp: 2\n[warn]\nwarn_command_abusers: yes\n[warn_reasons]\nnocmd: 90s, do not use commands you do not have access to, try using !help\n')
        self.player.connects('0')
        with patch.object(self.p, 'info') as (info_mock):
            self.player.says('!help')
            self.player.says('!help')
            self.player.says('!help')
        self.assertListEqual([call('ThePlayer does not have sufficient rights to use !help. Required level: 2'),
         call('ThePlayer does not have sufficient rights to use !help. Required level: 2')], info_mock.mock_calls)
        self.assertListEqual(['You do not have sufficient access to use !help',
         'You do not have sufficient access to use !help'], self.player.message_history)
        self.assertListEqual([
         call(1.5, 'do not use commands you do not have access to, try using !help', 'nocmd', ANY, ANY)], self.player_warn_mock.mock_calls)

    def test_warn_no__unknown_cmd(self, sleep_mock):
        self.init('\n[commands]\nhelp: 0\n[warn]\nwarn_command_abusers: no\n')
        self.assertFalse(self.p._warn_command_abusers)
        self.player.connects('0')
        self.player.says('!hzlp')
        self.assertListEqual(['Unrecognized command hzlp. Did you mean !help?'], self.player.message_history)
        self.assertFalse(self.player_warn_mock.called)

    def test_warn_yes__unknown_cmd(self, sleep_mock):
        self.init('\n[commands]\nhelp: 0\n[warn]\nwarn_command_abusers: yes\n')
        self.assertTrue(self.p._warn_command_abusers)
        self.player.connects('0')
        self.player.says('!hzlp')
        self.assertListEqual(['Unrecognized command hzlp. Did you mean !help?'], self.player.message_history)
        self.assertFalse(self.player_warn_mock.called)

    def test_warn_yes__unknown_cmd_abuser(self, sleep_mock):
        self.init('\n[commands]\nhelp: 0\n[warn]\nwarn_command_abusers: yes\n[warn_reasons]\nfakecmd: 2h, do not use fake commands\n')
        self.assertTrue(self.p._warn_command_abusers)
        self.player.connects('0')
        self.player.setvar(self.p, 'fakeCommand', 2)
        self.player.says('!hzlp')
        self.player.says('!hzlp')
        self.player.says('!hzlp')
        self.assertListEqual(['Unrecognized command hzlp. Did you mean !help?',
         'Unrecognized command hzlp. Did you mean !help?',
         'Unrecognized command hzlp. Did you mean !help?'], self.player.message_history)
        self.assertListEqual([call(120.0, 'do not use fake commands', 'fakecmd', ANY, ANY)], self.player_warn_mock.mock_calls)


@patch('time.sleep')
class Test_command_parsing(Admin_functional_test):

    def setUp(self):
        Admin_functional_test.setUp(self)
        self.init('\n[commands]\nhelp: 0\n')
        self.joe.connects('0')

    def test_normal_chat(self, sleep_mock):
        self.joe.says('f00')
        self.assertListEqual([], self.joe.message_history)
        self.joe.says('!help')
        self.assertListEqual(['Available commands: help, iamgod'], self.joe.message_history)

    def test_team_chat(self, sleep_mock):
        self.joe.says('f00')
        self.assertListEqual([], self.joe.message_history)
        self.joe.says2team('!help')
        self.assertListEqual(['Available commands: help, iamgod'], self.joe.message_history)

    def test_squad_chat(self, sleep_mock):
        self.joe.says('f00')
        self.assertListEqual([], self.joe.message_history)
        self.joe.says2squad('!help')
        self.assertListEqual(['Available commands: help, iamgod'], self.joe.message_history)

    def test_private_chat(self, sleep_mock):
        self.joe.says('f00')
        self.assertListEqual([], self.joe.message_history)
        self.joe.says2private('!help')
        self.assertListEqual(['Available commands: help, iamgod'], self.joe.message_history)


class Cmd_kick(Admin_functional_test):

    def setUp(self):
        Admin_functional_test.setUp(self)
        self.init()
        self.joe.connects('0')
        self.kick_patcher = patch.object(self.console, 'kick')
        self.kick_mock = self.kick_patcher.start()

    def tearDown(self):
        Admin_functional_test.tearDown(self)
        self.kick_patcher.stop()

    def test_no_parameter(self):
        self.joe.says('!kick')
        self.assertListEqual(['Invalid parameters'], self.joe.message_history)
        self.assertListEqual([], self.kick_mock.mock_calls)

    def test_self_kick(self):
        with patch.object(self.console, 'say') as (say_mock):
            self.joe.says('!kick joe')
        self.assertListEqual([], self.kick_mock.mock_calls)
        self.assertListEqual([call("^7Joe^7 ^7Can't kick yourself newb!")], say_mock.mock_calls)

    def test_no_reason_when_required(self):
        self.joe._groupBits = 16
        self.joe.says('!kick f00')
        self.assertListEqual(['ERROR: You must supply a reason'], self.joe.message_history)
        self.assertListEqual([], self.kick_mock.mock_calls)

    def test_kick_higher_level_admin(self):
        self.mike._groupBits = 16
        self.mike.connects('1')
        with patch.object(self.console, 'say') as (say_mock):
            self.mike.says('!kick joe reason1')
        self.assertListEqual([call("^7Joe^7^7 gets 1 point, Mike^7^7 gets none, Joe^7^7 wins, can't kick")], say_mock.mock_calls)
        self.assertListEqual([], self.kick_mock.mock_calls)

    def test_kick_masked_higher_level_admin(self):
        self.mike._groupBits = 16
        self.mike.connects('1')
        self.joe.says('!mask reg')
        self.mike.says('!kick joe reason1')
        self.assertListEqual(['Joe is a masked higher level player, action cancelled'], self.mike.message_history)
        self.assertListEqual([], self.kick_mock.mock_calls)

    def test_existing_player_name(self):
        self.mike.connects('1')
        self.joe.says('!kick mike the reason')
        self.assertListEqual([call(self.mike, 'the reason', self.joe, False)], self.kick_mock.mock_calls)
        self.assertEqual(1, self.console.storage.numPenalties(self.mike, 'Kick'))

    def test_unknown_player_name(self):
        self.mike.connects('6')
        self.joe.says('!kick f00')
        self.assertListEqual(['No players found matching f00'], self.joe.message_history)
        self.assertListEqual([], self.kick_mock.mock_calls)

    def test_kick_by_slot_id(self):
        self.mike.connects('6')
        self.joe.says('!kick 6')
        self.assertListEqual([call(self.mike, '', self.joe, False)], self.kick_mock.mock_calls)
        self.assertEqual(1, self.console.storage.numPenalties(self.mike, 'Kick'))

    def test_kick_by_slot_id_when_no_known_player_is_on_that_slot(self):
        self.mike.connects('6')
        self.joe.says('!kick 4')
        self.assertListEqual([call('4', '', self.joe)], self.kick_mock.mock_calls)

    def test_kick_by_database_id(self):
        self.mike.connects('6')
        mike_from_db = self.console.storage.getClient(Client(guid=self.mike.guid))
        self.assertIsNotNone(mike_from_db)
        self.joe.says('!kick @%s' % mike_from_db.id)
        self.assertListEqual([call(ANY, '', self.joe, False)], self.kick_mock.mock_calls)
        kick_call = self.kick_mock.mock_calls[0]
        kicked_player = kick_call[1][0]
        self.assertIsNotNone(kicked_player)
        self.assertIsNotNone(kicked_player.cid)

    def test_existing_player_by_name_containing_spaces(self):
        self.mike.connects('1')
        self.mike.name = 'F 0 0'
        self.joe.says('!kick f00 the reason')
        self.assertListEqual([call(self.mike, 'the reason', self.joe, False)], self.kick_mock.mock_calls)

    def test_existing_player_by_name_containing_spaces_2(self):
        self.mike.connects('1')
        self.mike.name = 'F 0 0'
        self.joe.says("!kick 'f 0 0' the reason")
        self.assertListEqual([call(self.mike, 'the reason', self.joe, False)], self.kick_mock.mock_calls)


class Cmd_spam(Admin_functional_test):

    def setUp(self):
        Admin_functional_test.setUp(self)
        self.init()
        self.joe.connects(0)
        self.mike.connects(1)

    def test_no_parameter(self):
        with patch.object(self.console, 'say') as (say_mock):
            self.joe.says('!spam')
        self.assertListEqual([], say_mock.mock_calls)
        self.assertListEqual(['Invalid parameters'], self.joe.message_history)

    def test_unknown_spammage_keyword(self):
        with patch.object(self.console, 'say') as (say_mock):
            self.joe.says('!spam f00')
        self.assertListEqual([], say_mock.mock_calls)
        self.assertListEqual(['Could not find spam message f00'], self.joe.message_history)

    def test_nominal_to_all_players(self):
        with patch.object(self.console, 'say') as (say_mock):
            self.joe.says('!spam rule1')
        self.assertListEqual([call('^3Rule #1: No racism of any kind')], say_mock.mock_calls)
        self.assertListEqual([], self.joe.message_history)

    def test_nominal_to_mike(self):
        with patch.object(self.console, 'say') as (say_mock):
            self.joe.says('!spam mike rule1')
        self.assertListEqual([], say_mock.mock_calls)
        self.assertListEqual([], self.joe.message_history)
        self.assertListEqual(['Rule #1: No racism of any kind'], self.mike.message_history)

    def test_nominal_to_unknown_player(self):
        with patch.object(self.console, 'say') as (say_mock):
            self.joe.says('!spam f00 rule1')
        self.assertListEqual([], say_mock.mock_calls)
        self.assertListEqual(['No players found matching f00'], self.joe.message_history)
        self.assertListEqual([], self.mike.message_history)

    def test_nominal_to_all_players_big(self):
        with patch.object(self.console, 'saybig') as (saybig_mock):
            self.joe.says('&spam rule1')
        self.assertListEqual([call('^3Rule #1: No racism of any kind')], saybig_mock.mock_calls)
        self.assertListEqual([], self.joe.message_history)