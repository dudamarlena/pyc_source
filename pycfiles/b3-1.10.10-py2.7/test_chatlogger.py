# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: H:\workspaces\workspace-python\big-brother-bot\tests\plugins\test_chatlogger.py
# Compiled at: 2015-05-27 19:37:28
import b3, b3.events, os, re, time, unittest2 as unittest, threading, sys, codecs
from mockito import when, unstub
from mock import Mock, ANY
from b3 import TEAM_RED, TEAM_BLUE
from b3.config import XmlConfigParser
from b3.config import CfgConfigParser
from b3.plugins.admin import AdminPlugin
from b3.plugins.chatlogger import ChatloggerPlugin
from tests import logging_disabled
from textwrap import dedent
from tempfile import mkdtemp
testcase_lock = threading.Lock()

def flush_console_streams():
    sys.stderr.flush()
    sys.stdout.flush()


def cleanUp():
    unstub()
    flush_console_streams()
    testcase_lock.release()


class ChatloggerTestCase(unittest.TestCase):

    def setUp(self):
        testcase_lock.acquire()
        self.addCleanup(cleanUp)
        flush_console_streams()
        self.parser_conf = XmlConfigParser()
        self.parser_conf.loadFromString('<configuration/>')
        with logging_disabled():
            from b3.fake import FakeConsole
            self.console = FakeConsole(self.parser_conf)
        with logging_disabled():
            self.adminPlugin = AdminPlugin(self.console, '@b3/conf/plugin_admin.ini')
            self.adminPlugin.onStartup()
        when(self.console).getPlugin('admin').thenReturn(self.adminPlugin)
        self.console.screen = Mock()
        self.console.time = time.time
        self.console.upTime = Mock(return_value=3)

    def tearDown(self):
        try:
            self.console.storage.shutdown()
        except:
            pass


with logging_disabled():
    from b3.fake import FakeClient

    def sendsPM(self, msg, target):
        self.console.queueEvent(self.console.getEvent('EVT_CLIENT_PRIVATE_SAY', msg, self, target))


    FakeClient.sendsPM = sendsPM

class Test_chatlogfile(ChatloggerTestCase):

    def setUp(self):
        ChatloggerTestCase.setUp(self)
        with logging_disabled():
            self.console.startup()
            self.conf = CfgConfigParser()
            self.p = ChatloggerPlugin(self.console, self.conf)
        when(self.console.config).get('b3', 'time_zone').thenReturn('GMT')
        self.conf.loadFromString(dedent('\n            [general]\n            save_to_database: no\n            save_to_file: yes\n\n            [file]\n            logfile: @conf/chat.log\n            rotation_rate: D\n\n            [purge]\n            max_age: 0\n            hour: 0\n            min: 0\n        '))
        self.temp_conf_folder = mkdtemp(suffix='b3_conf')
        when(b3).getConfPath(decode=ANY).thenReturn(self.temp_conf_folder)
        with logging_disabled():
            self.p.onLoadConfig()
            self.p.onStartup()
        self.chat_log_file = os.path.join(self.temp_conf_folder, 'chat.log')
        with logging_disabled():
            self.joe = FakeClient(self.console, name='Joe', guid='joe_guid', team=TEAM_RED)
            self.simon = FakeClient(self.console, name='Simon', guid='simon_guid', team=TEAM_BLUE)
            self.joe.connects(1)
            self.simon.connects(3)

    def get_all_chatlog_lines_from_logfile(self):
        lines = []
        with codecs.open(self.chat_log_file, 'r', encoding='utf-8') as (f):
            for l in f.readlines():
                lines.append(l.strip())

        return lines

    def count_chatlog_lines(self):
        return len(self.get_all_chatlog_lines_from_logfile())

    def assert_log_line(self, line, expected):
        """
        remove time stamp at the beginning of the line and compare the remainder
        """
        clean_line = re.sub('^\\d+-\\d+-\\d+ \\d\\d:\\d\\d:\\d\\d\\t', '', line)
        self.assertEqual(clean_line, expected)

    def test_global_chat(self):
        self.joe.says('hello')
        self.assertEqual(1, self.count_chatlog_lines())
        self.assert_log_line(self.get_all_chatlog_lines_from_logfile()[0], '@1 [Joe] to ALL:\thello')

    def test_team_chat(self):
        self.joe.says2team('hello')
        self.assertEqual(1, self.count_chatlog_lines())
        self.assert_log_line(self.get_all_chatlog_lines_from_logfile()[0], '@1 [Joe] to TEAM:\thello')

    @unittest.skipUnless(hasattr(FakeClient, 'says2squad'), 'FakeClient.says2squad not available in this version of B3')
    def test_squad_chat(self):
        self.joe.says2squad('hi')
        self.assertEqual(1, self.count_chatlog_lines())
        self.assert_log_line(self.get_all_chatlog_lines_from_logfile()[0], '@1 [Joe] to SQUAD:\thi')

    def test_private_chat(self):
        self.joe.sendsPM('hi', self.simon)
        self.assertEqual(1, self.count_chatlog_lines())
        self.assert_log_line(self.get_all_chatlog_lines_from_logfile()[0], '@1 [Joe] to PM:\thi')

    def test_unicode(self):
        self.joe.name = '★joe★'
        self.simon.name = '❮❮simon❯❯'
        self.joe.sendsPM('hi ✪', self.simon)
        self.assertEqual(1, self.count_chatlog_lines())
        self.assert_log_line(self.get_all_chatlog_lines_from_logfile()[0], '@1 [★joe★] to PM:\thi ✪')


class Test_Config(ChatloggerTestCase):

    def setUp(self):
        ChatloggerTestCase.setUp(self)
        with logging_disabled():
            self.console.startup()
        self.conf = CfgConfigParser()
        self.p = ChatloggerPlugin(self.console, self.conf)
        when(self.console.config).get('b3', 'time_zone').thenReturn('GMT')
        self.p.setup_fileLogger = Mock()

    def init(self, config_content=None):
        """ load plugin config and initialise the plugin """
        if config_content:
            self.conf.loadFromString(config_content)
        elif os.path.isfile(b3.getAbsolutePath('@b3/conf/plugin_chatlogger.ini')):
            self.conf.load(b3.getAbsolutePath('@b3/conf/plugin_chatlogger.ini'))
        else:
            raise unittest.SkipTest("default config file '%s' does not exists" % b3.getAbsolutePath('@b3/conf/plugin_chatlogger.ini'))
        self.p.onLoadConfig()
        self.p.onStartup()

    def test_default_config(self):
        when(b3).getB3Path(decode=ANY).thenReturn('c:\\b3_folder')
        when(b3).getConfPath(decode=ANY).thenReturn('c:\\b3_conf_folder')
        self.init()
        self.assertTrue(self.p._save2db)
        self.assertTrue(self.p._save2file)
        expected_log_file = 'c:\\b3_conf_folder\\chat.log' if sys.platform == 'win32' else 'c:\\b3_conf_folder/chat.log'
        self.assertEqual(expected_log_file, self.p._file_name)
        self.assertEqual('D', self.p._file_rotation_rate)
        self.assertEqual(0, self.p._max_age_in_days)
        self.assertEqual(0, self.p._max_age_cmd_in_days)
        self.assertEqual(0, self.p._hours)
        self.assertEqual(0, self.p._minutes)

    def test_empty_config(self):
        self.init('\n        ')
        self.assertTrue(self.p._save2db)
        self.assertFalse(self.p._save2file)
        self.assertIsNone(self.p._file_name)
        self.assertIsNone(self.p._file_rotation_rate)
        self.assertEqual(0, self.p._max_age_in_days)
        self.assertEqual(0, self.p._max_age_cmd_in_days)
        self.assertEqual(0, self.p._hours)
        self.assertEqual(0, self.p._minutes)
        self.assertEqual('chatlog', self.p._db_table)
        self.assertEqual('cmdlog', self.p._db_table_cmdlog)

    def test_conf1(self):
        self.init(dedent('\n            [purge]\n            max_age:7d\n            hour:4\n            min:0\n        '))
        self.assertTrue(self.p._save2db)
        self.assertFalse(self.p._save2file)
        self.assertIsNone(self.p._file_name)
        self.assertIsNone(self.p._file_rotation_rate)
        self.assertEqual(7, self.p._max_age_in_days)
        self.assertEqual(0, self.p._max_age_cmd_in_days)
        self.assertEqual(4, self.p._hours)
        self.assertEqual(0, self.p._minutes)