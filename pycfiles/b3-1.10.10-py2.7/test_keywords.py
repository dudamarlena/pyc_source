# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\tests\plugins\adv\test_keywords.py
# Compiled at: 2016-03-08 18:42:10
import StringIO, feedparser
from b3.fake import FakeClient
from mock import patch, call, Mock
from mockito import when, any as ANY
from tests.plugins.adv import AdvTestCase, RSS_FEED_CONTENT

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