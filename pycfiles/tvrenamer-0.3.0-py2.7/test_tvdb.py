# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-2.2.1-i686/egg/tvrenamer/tests/services/test_tvdb.py
# Compiled at: 2015-11-08 18:31:47
import os, testtools
from tvrenamer.services import tvdb
from tvrenamer.tests import base

def disabled():
    return not os.environ.get('TEST_TVDB_API_KEY') or not os.environ.get('TEST_TVDB_API_USER') or not os.environ.get('TEST_TVDB_API_PASSWORD')


class TvdbServiceTest(base.BaseTest):

    def setUp(self):
        super(TvdbServiceTest, self).setUp()
        self.CONF.set_override('apikey', os.environ.get('TEST_TVDB_API_KEY'), 'tvdb')
        self.CONF.set_override('username', os.environ.get('TEST_TVDB_API_USER'), 'tvdb')
        self.CONF.set_override('userpass', os.environ.get('TEST_TVDB_API_PASSWORD'), 'tvdb')
        self.CONF.set_override('select_first', True, 'tvdb')
        self.api = tvdb.TvdbService()

    @testtools.skipIf(disabled(), 'live api testing disabled')
    def test_get_series_by_name(self):
        series, err = self.api.get_series_by_name('The Big Bang Theory')
        self.assertIsNotNone(series)
        self.assertIsNone(err)
        self.assertEqual(series['seriesName'], 'The Big Bang Theory')
        series, err = self.api.get_series_by_name('Fake - Unknown Series')
        self.assertIsNone(series)
        self.assertIsNotNone(err)
        self.assertEqual(err, 'Not Found')

    @testtools.skipIf(disabled(), 'live api testing disabled')
    def test_get_series_by_id(self):
        series, err = self.api.get_series_by_id(80379)
        self.assertIsNotNone(series)
        self.assertIsNone(err)
        self.assertEqual(series['seriesName'], 'The Big Bang Theory')
        series, err = self.api.get_series_by_id(0)
        self.assertIsNone(series)
        self.assertIsNotNone(err)
        self.assertEqual(err, 'Not Found')

    @testtools.skipIf(disabled(), 'live api testing disabled')
    def test_get_series_name(self):
        series, err = self.api.get_series_by_name('The Big Bang Theory')
        self.assertIsNotNone(series)
        self.assertIsNone(err)
        self.assertEqual(self.api.get_series_name(series), 'The Big Bang Theory')

    @testtools.skipIf(disabled(), 'live api testing disabled')
    def test_get_episode_name(self):
        series, err = self.api.get_series_by_name('The Big Bang Theory')
        episodes, eperr = self.api.get_episode_name(series, [1], 1)
        self.assertIsNotNone(episodes)
        self.assertIsNone(eperr)
        self.assertEqual(episodes, ['Pilot'])

    @testtools.skipIf(disabled(), 'live api testing disabled')
    def test_get_episode_name_season_nf(self):
        series, err = self.api.get_series_by_name('Firefly')
        episodes, eperr = self.api.get_episode_name(series, [1], 2)
        self.assertIsNone(episodes)
        self.assertIsNotNone(eperr)
        self.assertEqual(eperr, 'Not Found')

    @testtools.skipIf(disabled(), 'live api testing disabled')
    def test_get_episode_name_attr_nf(self):
        series, err = self.api.get_series_by_name('Firefly')
        episodes, eperr = self.api.get_episode_name(series, [1], 5)
        self.assertIsNone(episodes)
        self.assertIsNotNone(eperr)
        self.assertEqual(eperr, 'Not Found')

    @testtools.skipIf(disabled(), 'live api testing disabled')
    def test_get_episode_name_episode_nf(self):
        series, err = self.api.get_series_by_name('Firefly')
        episodes, eperr = self.api.get_episode_name(series, [25], 1)
        self.assertIsNone(episodes)
        self.assertIsNone(eperr)
        series, err = self.api.get_series_by_name('Firefly')
        episodes, eperr = self.api.get_episode_name(series, [15], 0)
        self.assertIsNotNone(episodes)
        self.assertIsNone(eperr)
        self.assertEqual(episodes, ['Serenity'])