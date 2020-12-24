# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\chatlogger\test_file.py
# Compiled at: 2016-03-08 18:42:10
import b3, b3.events, os, re, codecs
from mockito import when
from mock import ANY
from b3 import TEAM_RED, TEAM_BLUE
from b3.config import CfgConfigParser
from b3.plugins.chatlogger import ChatloggerPlugin
from tests import logging_disabled
from tests.plugins.chatlogger import ChatloggerTestCase
from textwrap import dedent
from tempfile import mkdtemp
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
        when(b3).getConfPath(decode=ANY, conf=None).thenReturn(self.temp_conf_folder)
        with logging_disabled():
            self.p.onLoadConfig()
            self.p.onStartup()
        self.chat_log_file = os.path.join(self.temp_conf_folder, 'chat.log')
        with logging_disabled():
            self.joe = FakeClient(self.console, name='Joe', guid='joe_guid', team=TEAM_RED)
            self.simon = FakeClient(self.console, name='Simon', guid='simon_guid', team=TEAM_BLUE)
            self.joe.connects(1)
            self.simon.connects(3)
        return

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