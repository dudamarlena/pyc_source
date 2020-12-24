# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: H:\workspaces\workspace-python\big-brother-bot\tests\plugins\test_adv.py
# Compiled at: 2015-03-08 21:04:34
import StringIO, logging, os
from mock import patch, call, Mock
from mockito import when, any as ANY, unstub
from b3.fake import FakeClient
import feedparser
from b3.plugins.admin import AdminPlugin
from tests import B3TestCase
import unittest2 as unittest
from b3.plugins.adv import AdvPlugin, MessageLoop
from b3.config import XmlConfigParser, CfgConfigParser
from b3 import __file__ as b3_module__file__
ADMIN_CONFIG_FILE = os.path.normpath(os.path.join(os.path.dirname(b3_module__file__), 'conf/plugin_admin.ini'))
ADMIN_CONFIG = None
default_plugin_file = os.path.normpath(os.path.join(os.path.dirname(__file__), '../../b3/conf/plugin_adv.xml'))
default_plugin_content = None
timer_patcher = None
RSS_FEED_CONTENT = '<?xml version="1.0" encoding="UTF-8"?>\n<rss version="0.92" xml:lang="en-US">\n    <channel>\n        <title>Big Brother Bot Forum - News (Read Only)</title>\n        <link>http://forum.bigbrotherbot.net/index.php</link>\n        <description><![CDATA[Live information from Big Brother Bot Forum]]></description>\n        <item>\n            <title>f00 bar item title</title>\n            <link>http://forum.bigbrotherbot.net/news-2/f00-item-link</link>\n            <description>\n                <![CDATA[f00 bar item description]]>\n            </description>\n            <pubDate>Sun, 08 Feb 2015 08:53:37 GMT</pubDate>\n            <guid>http://forum.bigbrotherbot.net/news-2/123456798</guid>\n        </item>\n    </channel>\n</rss>\n'

def setUpModule():
    global ADMIN_CONFIG
    global ADMIN_CONFIG_FILE
    global default_plugin_content
    global default_plugin_file
    global timer_patcher
    if os.path.exists(default_plugin_file):
        with open(default_plugin_file, 'r') as (f):
            default_plugin_content = f.read()
    ADMIN_CONFIG = CfgConfigParser()
    ADMIN_CONFIG.load(ADMIN_CONFIG_FILE)
    timer_patcher = patch('threading.Timer')
    timer_patcher.start()


def tearDownModule():
    timer_patcher.stop()


class AdvTestCase(B3TestCase):
    """ Ease test cases that need an working B3 console and need to control the ADV plugin config """

    def setUp(self):
        self.log = logging.getLogger('output')
        self.log.propagate = False
        B3TestCase.setUp(self)
        self.adminPlugin = AdminPlugin(self.console, ADMIN_CONFIG)
        when(self.console).getPlugin('admin').thenReturn(self.adminPlugin)
        self.adminPlugin.onLoadConfig()
        self.adminPlugin.onStartup()
        self.console.startup()
        self.log.propagate = True

    def tearDown(self):
        B3TestCase.tearDown(self)
        unstub()

    def init_plugin(self, config_content=None):
        conf = None
        if config_content:
            conf = XmlConfigParser()
            conf.setXml(config_content)
        elif default_plugin_content:
            conf = XmlConfigParser()
            conf.setXml(default_plugin_content)
        else:
            unittest.skip('cannot get default plugin config file at %s' % default_plugin_file)
        self.p = AdvPlugin(self.console, conf)
        self.p.save = Mock()
        self.conf = self.p.config
        self.log.setLevel(logging.DEBUG)
        self.log.info('============================= Adv plugin: loading config ============================')
        self.p.onLoadConfig()
        self.log.info('============================= Adv plugin: starting  =================================')
        self.p.onStartup()
        return


class Test_config(AdvTestCase):

    def test_default_config(self):
        self.init_plugin()
        self.assertEqual('2', self.p._rate)
        self.assertIsNone(self.p._fileName)
        self.assertEqual('http://forum.bigbrotherbot.net/news-2/?type=rss;action=.xml', self.p._feed)
        self.assertEqual('News: ', self.p._feedpre)
        self.assertEqual(4, self.p._feedmaxitems)
        self.assertEqual('News: ', self.p._feedpre)
        self.assertIsNotNone(self.p._cronTab)
        self.assertTupleEqual((0, range(0, 59, 2), -1, -1, -1, -1), (
         self.p._cronTab.second, self.p._cronTab.minute, self.p._cronTab.hour,
         self.p._cronTab.day, self.p._cronTab.month, self.p._cronTab.dow))
        self.assertEqual(10, len(self.p._msg.items))
        self.assertListEqual([
         '^2Big Brother Bot is watching you... www.BigBrotherBot.net',
         '@feed',
         'server watched by @admins',
         '^3Rule #1: No racism of any kind',
         '@time',
         '@admins',
         '@feed',
         '^2Do you like B3? Consider donating to the project at www.BigBrotherBot.net',
         '@nextmap',
         '@topstats'], self.p._msg.items)

    def test_empty(self):
        self.init_plugin('<configuration plugin="adv" />')
        self.assertEqual(self.p._rate, '2')
        self.assertIsNone(self.p._fileName)
        self.assertEqual(0, len(self.p._msg.items))
        self.assertEqual('http://forum.bigbrotherbot.net/news-2/?type=rss;action=.xml', self.p._feed)
        self.assertEqual('News: ', self.p._feedpre)
        self.assertEqual(4, self.p._feedmaxitems)
        self.assertEqual('News: ', self.p._feedpre)
        self.assertIsNotNone(self.p._cronTab)

    def test_rate_nominal(self):
        self.init_plugin('<configuration plugin="adv">\n    <settings name="settings">\n        <set name="rate">1</set>\n    </settings>\n</configuration>\n')
        self.assertEqual('1', self.p._rate)
        self.assertIsNotNone(self.p._cronTab)
        self.assertTupleEqual((0, range(60), -1, -1, -1, -1), (
         self.p._cronTab.second, self.p._cronTab.minute, self.p._cronTab.hour,
         self.p._cronTab.day, self.p._cronTab.month, self.p._cronTab.dow))

    def test_rate_nominal_second(self):
        self.init_plugin('<configuration plugin="adv">\n    <settings name="settings">\n        <set name="rate">40s</set>\n    </settings>\n</configuration>\n')
        self.assertEqual('40s', self.p._rate)
        self.assertIsNotNone(self.p._cronTab)
        self.assertTupleEqual(([0, 40], -1, -1, -1, -1, -1), (
         self.p._cronTab.second, self.p._cronTab.minute, self.p._cronTab.hour,
         self.p._cronTab.day, self.p._cronTab.month, self.p._cronTab.dow))

    def test_rate_junk(self):
        try:
            self.init_plugin('<configuration plugin="adv">\n    <settings name="settings">\n        <set name="rate">f00</set>\n    </settings>\n</configuration>\n')
        except TypeError as err:
            print err
        except Exception:
            raise

        self.assertEqual('f00', self.p._rate)
        self.assertIsNone(self.p._cronTab)


class Test_commands(AdvTestCase):

    def setUp(self):
        AdvTestCase.setUp(self)
        self.joe = FakeClient(self.console, name='Joe', guid='joeguid', groupBits=128)

    def tearDown(self):
        AdvTestCase.tearDown(self)

    def test_advlist_empty(self):
        self.init_plugin('\n            <configuration>\n                <settings name="settings">\n                    <set name="rate">30s</set>\n                </settings>\n                <ads>\n                </ads>\n            </configuration>\n        ')
        self.joe.clearMessageHistory()
        self.p.cmd_advlist(data=None, client=self.joe)
        self.assertEqual([], self.p._msg.items)
        self.assertEqual(['Adv: no ads loaded'], self.joe.message_history)
        return

    def test_advlist_one_item(self):
        self.init_plugin('\n            <configuration>\n                <settings name="settings">\n                    <set name="rate">30s</set>\n                </settings>\n                <ads>\n                    <ad>f00</ad>\n                </ads>\n            </configuration>\n        ')
        self.joe.clearMessageHistory()
        self.p.cmd_advlist(data=None, client=self.joe)
        self.assertEqual(['f00'], self.p._msg.items)
        self.assertEqual(['Adv: [1] f00'], self.joe.message_history)
        return

    def test_advlist_many_items(self):
        self.init_plugin('\n            <configuration>\n                <settings name="settings">\n                    <set name="rate">30s</set>\n                </settings>\n                <ads>\n                    <ad>f00</ad>\n                    <ad>bar</ad>\n                    <ad>test</ad>\n                </ads>\n            </configuration>\n        ')
        self.joe.clearMessageHistory()
        self.p.cmd_advlist(data=None, client=self.joe)
        self.assertEqual(['f00', 'bar', 'test'], self.p._msg.items)
        self.assertEqual(['Adv: [1] f00', 'Adv: [2] bar', 'Adv: [3] test'], self.joe.message_history)
        return

    def test_advrate_no_arg_30s(self):
        self.init_plugin('\n            <configuration>\n                <settings name="settings">\n                    <set name="rate">30s</set>\n                </settings>\n                <ads>\n                    <ad>f00</ad>\n                    <ad>bar</ad>\n                    <ad>test</ad>\n                </ads>\n            </configuration>\n        ')
        self.joe.clearMessageHistory()
        self.p.cmd_advrate(data='', client=self.joe)
        self.assertEqual('30s', self.p._rate)
        self.assertEqual(['Current rate is every 30 seconds'], self.joe.message_history)

    def test_advrate_no_arg_2min(self):
        self.init_plugin('\n            <configuration>\n                <settings name="settings">\n                    <set name="rate">2</set>\n                </settings>\n                <ads>\n                    <ad>f00</ad>\n                    <ad>bar</ad>\n                    <ad>test</ad>\n                </ads>\n            </configuration>\n        ')
        self.joe.clearMessageHistory()
        self.p.cmd_advrate(data=None, client=self.joe)
        self.assertEqual('2', self.p._rate)
        self.assertEqual(['Current rate is every 2 minutes'], self.joe.message_history)
        return

    def test_advrate_set_20s(self):
        self.init_plugin('\n            <configuration>\n                <settings name="settings">\n                    <set name="rate">45s</set>\n                </settings>\n                <ads>\n                    <ad>f00</ad>\n                    <ad>bar</ad>\n                    <ad>test</ad>\n                </ads>\n            </configuration>\n        ')
        self.assertEqual('45s', self.p._rate)
        self.joe.clearMessageHistory()
        self.p.cmd_advrate(data='20s', client=self.joe)
        self.assertEqual('20s', self.p._rate)
        self.assertEqual(['Adv: rate set to 20 seconds'], self.joe.message_history)

    def test_advrate_set_3min(self):
        self.init_plugin('\n            <configuration>\n                <settings name="settings">\n                    <set name="rate">45s</set>\n                </settings>\n                <ads>\n                    <ad>f00</ad>\n                    <ad>bar</ad>\n                    <ad>test</ad>\n                </ads>\n            </configuration>\n        ')
        self.assertEqual('45s', self.p._rate)
        self.joe.clearMessageHistory()
        self.p.cmd_advrate(data='3', client=self.joe)
        self.assertEqual('3', self.p._rate)
        self.assertEqual(['Adv: rate set to 3 minutes'], self.joe.message_history)

    def test_advrem_nominal(self):
        self.init_plugin('\n            <configuration>\n                <settings name="settings">\n                    <set name="rate">45s</set>\n                </settings>\n                <ads>\n                    <ad>f00</ad>\n                    <ad>bar</ad>\n                    <ad>test</ad>\n                </ads>\n            </configuration>\n        ')
        self.assertEqual(['f00', 'bar', 'test'], self.p._msg.items)
        self.joe.clearMessageHistory()
        self.p.cmd_advrem(data='2', client=self.joe)
        self.assertEqual(['f00', 'test'], self.p._msg.items)
        self.assertEqual(['Adv: removed item: bar'], self.joe.message_history)

    def test_advrem_no_arg(self):
        self.init_plugin('\n            <configuration>\n                <settings name="settings">\n                    <set name="rate">45s</set>\n                </settings>\n                <ads>\n                    <ad>f00</ad>\n                    <ad>bar</ad>\n                    <ad>test</ad>\n                </ads>\n            </configuration>\n        ')
        self.assertEqual(['f00', 'bar', 'test'], self.p._msg.items)
        self.joe.clearMessageHistory()
        self.p.cmd_advrem(data=None, client=self.joe)
        self.assertEqual(['f00', 'bar', 'test'], self.p._msg.items)
        self.assertEqual(['Missing data, try !help advrem'], self.joe.message_history)
        return

    def test_advrem_junk(self):
        self.init_plugin('\n            <configuration>\n                <settings name="settings">\n                    <set name="rate">45s</set>\n                </settings>\n                <ads>\n                    <ad>f00</ad>\n                    <ad>bar</ad>\n                    <ad>test</ad>\n                </ads>\n            </configuration>\n        ')
        self.assertEqual(['f00', 'bar', 'test'], self.p._msg.items)
        self.joe.clearMessageHistory()
        self.p.cmd_advrem(data='f00', client=self.joe)
        self.assertEqual(['f00', 'bar', 'test'], self.p._msg.items)
        self.assertEqual(['Invalid data, use the !advlist command to list valid items numbers'], self.joe.message_history)

    def test_advrem_invalid_index(self):
        self.init_plugin('\n            <configuration>\n                <settings name="settings">\n                    <set name="rate">45s</set>\n                </settings>\n                <ads>\n                    <ad>f00</ad>\n                    <ad>bar</ad>\n                    <ad>test</ad>\n                </ads>\n            </configuration>\n        ')
        self.assertEqual(['f00', 'bar', 'test'], self.p._msg.items)
        self.joe.clearMessageHistory()
        self.p.cmd_advrem(data='-18', client=self.joe)
        self.assertEqual(['f00', 'bar', 'test'], self.p._msg.items)
        self.assertEqual(['Invalid data, use the !advlist command to list valid items numbers'], self.joe.message_history)

    def test_advadd_nominal(self):
        self.init_plugin('\n            <configuration>\n                <settings name="settings">\n                    <set name="rate">45s</set>\n                </settings>\n                <ads>\n                    <ad>f00</ad>\n                </ads>\n            </configuration>\n        ')
        self.assertEqual(['f00'], self.p._msg.items)
        self.joe.clearMessageHistory()
        self.p.cmd_advadd(data='bar', client=self.joe)
        self.assertEqual(['f00', 'bar'], self.p._msg.items)
        self.assertEqual(['Adv: "bar" added'], self.joe.message_history)

    def test_advadd_no_arg(self):
        self.init_plugin('\n            <configuration>\n                <settings name="settings">\n                    <set name="rate">45s</set>\n                </settings>\n                <ads>\n                    <ad>f00</ad>\n                </ads>\n            </configuration>\n        ')
        self.assertEqual(['f00'], self.p._msg.items)
        self.joe.clearMessageHistory()
        self.p.cmd_advadd(data=None, client=self.joe)
        self.assertEqual(['f00'], self.p._msg.items)
        self.assertEqual(['Missing data, try !help advadd'], self.joe.message_history)
        return


class Test_keywords(AdvTestCase):

    def setUp(self):
        AdvTestCase.setUp(self)
        self.init_plugin()

    def test_admins(self):
        when(self.p._msg).getnext().thenReturn('@admins')
        joe = FakeClient(self.console, name='Joe', guid='joeguid', groupBits=128)
        when(self.p._adminPlugin).getAdmins().thenReturn([joe])
        with patch.object(self.console, 'say') as (say_mock):
            self.p.adv()
        say_mock.assert_has_calls([call('^7Admins online: Joe^7^7 [^3100^7]')])

    def test_regulars(self):
        when(self.p._msg).getnext().thenReturn('@regulars')
        joe = FakeClient(self.console, name='Joe', guid='joeguid', groupBits=2)
        when(self.p._adminPlugin).getRegulars().thenReturn([joe])
        with patch.object(self.console, 'say') as (say_mock):
            self.p.adv()
        say_mock.assert_has_calls([call('^7Regular players online: Joe^7')])

    def test_topstats(self):
        when(self.p._msg).getnext().thenReturn('@topstats')
        self.p._xlrstatsPlugin = Mock()
        with patch.object(self.p._xlrstatsPlugin, 'cmd_xlrtopstats') as (xlrtopstats_mock):
            self.p.adv()
            xlrtopstats_mock.assert_has_calls([call(ext=True, cmd=None, data='3', client=None)])
        return

    def test_time(self):
        when(self.p._msg).getnext().thenReturn('@time')
        when(self.console).formatTime(ANY()).thenReturn('f00')
        with patch.object(self.console, 'say') as (say_mock):
            self.p.adv()
            say_mock.assert_has_calls([call('^2Time: ^3f00')])

    def test_nextmap(self):
        when(self.p._msg).getnext().thenReturn('@nextmap')
        when(self.console).getNextMap().thenReturn('f00')
        with patch.object(self.console, 'say') as (say_mock):
            self.p.adv()
            say_mock.assert_has_calls([call('^2Next map: ^3f00')])

    def test_feed(self):
        self.p._feed = 'http://some.feed/rss'
        when(self.p._msg).getnext().thenReturn('@feed')
        with patch.object(feedparser, '_open_resource', return_value=StringIO.StringIO(RSS_FEED_CONTENT)):
            with patch.object(self.console, 'say') as (say_mock):
                self.p.adv()
                say_mock.assert_has_calls([call('News: f00 bar item title')])


class Test_MessageLoop(unittest.TestCase):

    def test_empty(self):
        ml = MessageLoop()
        self.assertEqual([], ml.items)
        self.assertEqual(None, ml.getnext())
        return

    def test_one_element(self):
        ml = MessageLoop()
        ml.items = ['f00']
        self.assertEqual('f00', ml.getnext())
        self.assertEqual('f00', ml.getnext())

    def test_three_elements(self):
        ml = MessageLoop()
        ml.items = ['f001', 'f002', 'f003']
        self.assertEqual('f001', ml.getnext())
        self.assertEqual('f002', ml.getnext())
        self.assertEqual('f003', ml.getnext())
        self.assertEqual('f001', ml.getnext())
        self.assertEqual('f002', ml.getnext())
        self.assertEqual('f003', ml.getnext())

    def test_put(self):
        ml = MessageLoop()
        self.assertEqual([], ml.items)
        ml.put('bar')
        self.assertEqual(['bar'], ml.items)

    def test_getitem(self):
        ml = MessageLoop()
        ml.items = ['f00']
        self.assertEqual('f00', ml.getitem(0))
        self.assertEqual(None, ml.getitem(1))
        return

    def test_remove(self):
        ml = MessageLoop()
        ml.items = ['f00', 'bar']
        self.assertEqual('f00', ml.getitem(0))
        ml.remove(0)
        self.assertEqual(['bar'], ml.items)
        self.assertEqual('bar', ml.getitem(0))

    def test_clear(self):
        ml = MessageLoop()
        ml.items = ['f00', 'bar']
        ml.clear()
        self.assertEqual([], ml.items)