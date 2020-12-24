# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: H:\workspaces\workspace-python\big-brother-bot\tests\plugins\test_translator.py
# Compiled at: 2015-05-27 19:37:28
import unittest2
from mockito import when
from b3.config import XmlConfigParser
from b3.config import CfgConfigParser
from b3.plugins.admin import AdminPlugin
from b3.plugins.translator import TranslatorPlugin
from tests import logging_disabled
from textwrap import dedent

class TranslatorTestCase(unittest2.TestCase):

    def setUp(self):
        self.parser_conf = XmlConfigParser()
        self.parser_conf.loadFromString('<configuration/>')
        with logging_disabled():
            from b3.fake import FakeConsole
            self.console = FakeConsole(self.parser_conf)
        with logging_disabled():
            self.adminPlugin = AdminPlugin(self.console, '@b3/conf/plugin_admin.ini')
            self.adminPlugin._commands = {}
            self.adminPlugin.onStartup()
        when(self.console).getPlugin('admin').thenReturn(self.adminPlugin)

    def tearDown(self):
        self.console.working = False


class Test_commands(TranslatorTestCase):

    def setUp(self):
        TranslatorTestCase.setUp(self)
        self.conf = CfgConfigParser()
        self.conf.loadFromString(dedent('\n            [settings]\n            default_source_language: it\n            default_target_language: en\n            display_translator_name: no\n            translator_name: ^7[^1T^7]\n            min_sentence_length: 6\n            microsoft_client_id: fakeclientid\n            microsoft_client_secret: fakeclientsecret\n\n            [commands]\n            translate: reg\n            translast: reg\n            transauto: reg\n            translang: reg\n        '))
        self.p = TranslatorPlugin(self.console, self.conf)
        self.p.onLoadConfig()
        self.p.onStartup()
        with logging_disabled():
            from b3.fake import FakeClient
        self.mike = FakeClient(console=self.console, name='Mike', guid='mikeguid', groupBits=2)
        self.bill = FakeClient(console=self.console, name='Bill', guid='billguid', groupBits=2)
        self.mike.connects('1')
        self.bill.connects('2')
        when(self.p).translate('it', 'en', 'Messaggio di prova').thenReturn('Test message')
        when(self.p).translate('en', 'fr', 'Test message').thenReturn('Message de test')
        when(self.p).translate('de', 'es', 'Test Meldungs').thenReturn('Mensaje de prueba')
        when(self.p).translate('nl', 'de', 'Test Bericht').thenReturn('Test Meldungs')
        when(self.p).translate('fr', 'en', 'Message de test').thenReturn('Test message')
        when(self.p).translate('it', 'es', 'Messaggio di prova').thenReturn('Mensaje de prueba')
        when(self.p).translate('', 'en', 'Messaggio di prova').thenReturn('Test message')
        when(self.p).translate('', 'fr', 'Messaggio di prova').thenReturn('Message de test')

    def test_cmd_translate_no_source_and_target(self):
        self.mike.clearMessageHistory()
        self.mike.says('!translate Messaggio di prova')
        self.assertListEqual(['Test message'], self.mike.message_history)

    def test_cmd_translate_with_source_and_target(self):
        self.mike.clearMessageHistory()
        self.mike.says('!translate en*fr Test message')
        self.assertListEqual(['Message de test'], self.mike.message_history)

    def test_cmd_translate_with_source_only(self):
        self.mike.clearMessageHistory()
        self.mike.says('!translate fr* Message de test')
        self.assertListEqual(['Test message'], self.mike.message_history)

    def test_cmd_translate_with_target_only(self):
        self.mike.clearMessageHistory()
        self.mike.says('!translate *es Messaggio di prova')
        self.assertListEqual(['Mensaje de prueba'], self.mike.message_history)

    def test_cmd_translast(self):
        self.bill.says('Messaggio di prova')
        self.mike.clearMessageHistory()
        self.mike.says('!translast')
        self.assertListEqual(['Test message'], self.mike.message_history)

    def test_cmd_translast_with_target(self):
        self.bill.says('Messaggio di prova')
        self.mike.clearMessageHistory()
        self.mike.says('!translast fr')
        self.assertListEqual(['Message de test'], self.mike.message_history)

    def test_cmd_transauto(self):
        self.mike.says('!transauto on')
        self.mike.clearMessageHistory()
        self.bill.says('Messaggio di prova')
        self.assertListEqual(['Test message'], self.mike.message_history)