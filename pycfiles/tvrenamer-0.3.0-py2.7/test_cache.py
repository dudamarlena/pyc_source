# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-2.2.1-i686/egg/tvrenamer/tests/processors/test_cache.py
# Compiled at: 2015-11-08 18:31:47
import os, tempfile, mock
from tvrenamer.processors import cache
from tvrenamer.tests import base

class CacheProcessorTests(base.BaseTest):

    def setUp(self):
        super(CacheProcessorTests, self).setUp()
        dbfile = os.path.join(tempfile.mkdtemp(), 'cache.json')
        self.CONF.set_override('dbfile', dbfile, 'cache')
        self.processor = cache.CacheResults()

    def _make_data(self):
        results = []
        ep1 = mock.Mock()
        ep1.status = {'/tmp/Lucy.2014.576p.BDRip.AC3.x264.DuaL-EAGLE.mkv': {'formatted_filename': None, 
                                                                 'state': 'failed', 
                                                                 'messages': 'Could not find season 20'}}
        results.append(ep1)
        ep2 = mock.Mock()
        ep2.status = {'/tmp/revenge.412.hdtv-lol.mp4': {'formatted_filename': 'S04E12-Madness.mp4', 
                                             'state': 'finished', 
                                             'messages': None}}
        results.append(ep2)
        return results

    @mock.patch('tvrenamer.cache.dbapi')
    def test_cache_result(self, mock_cache):
        self.CONF.set_override('cache_enabled', False)
        self.assertFalse(self.processor.enabled)
        self.processor.process([])
        self.assertFalse(mock_cache.called)
        self.CONF.set_override('cache_enabled', True)
        self.assertTrue(self.processor.enabled)
        self.processor.process(self._make_data())
        self.assertTrue(mock_cache.called)
        mock_cache.side_effect = RuntimeError
        self.processor.process(self._make_data())
        self.assertTrue(mock_cache.called)