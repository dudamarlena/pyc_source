# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-2.2.1-i686/egg/tvrenamer/tests/processors/test_base.py
# Compiled at: 2015-11-08 18:31:47
import os, tempfile, mock
from tvrenamer import processors
from tvrenamer.processors import cache
from tvrenamer.processors import noop
from tvrenamer.processors import printer
from tvrenamer.tests import base

class ProcessorBaseTests(base.BaseTest):

    def setUp(self):
        super(ProcessorBaseTests, self).setUp()
        dbfile = os.path.join(tempfile.mkdtemp(), 'cache.json')
        self.CONF.set_override('dbfile', dbfile, 'cache')

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

    def test_noop_only(self):
        self.CONF.set_override('cache_enabled', False)
        self.CONF.set_override('console_output_enabled', False)
        processor_mgr = processors.load()
        exts = processor_mgr.sorted_extensions()
        self.assertEqual(len(exts), 1)
        self.assertIsInstance(exts[0].obj, noop.NoopResults)
        processor_mgr.map_method('process', [])

    def test_printer(self):
        self.CONF.set_override('cache_enabled', False)
        self.CONF.set_override('console_output_enabled', True)
        processor_mgr = processors.load()
        exts = processor_mgr.sorted_extensions()
        self.assertEqual(len(exts), 2)
        self.assertIsInstance(exts[0].obj, printer.PrintResults)
        self.assertIsInstance(exts[1].obj, noop.NoopResults)

    def test_cache(self):
        self.CONF.set_override('cache_enabled', True)
        self.CONF.set_override('console_output_enabled', False)
        processor_mgr = processors.load()
        exts = processor_mgr.sorted_extensions()
        self.assertEqual(len(exts), 2)
        self.assertIsInstance(exts[0].obj, cache.CacheResults)
        self.assertIsInstance(exts[1].obj, noop.NoopResults)

    def test_all(self):
        self.CONF.set_override('cache_enabled', True)
        self.CONF.set_override('console_output_enabled', True)
        processor_mgr = processors.load()
        exts = processor_mgr.sorted_extensions()
        self.assertEqual(len(exts), 3)
        self.assertIsInstance(exts[0].obj, cache.CacheResults)
        self.assertIsInstance(exts[1].obj, printer.PrintResults)
        self.assertIsInstance(exts[2].obj, noop.NoopResults)

    def test_execute_all(self):
        self.CONF.set_override('cache_enabled', True)
        self.CONF.set_override('console_output_enabled', True)
        processor_mgr = processors.load()
        with mock.patch.object(cache.CacheResults, 'process', autospec=True) as (mock_cproc):
            with mock.patch.object(printer.PrintResults, 'process', autospec=True) as (mock_pproc):
                with mock.patch.object(noop.NoopResults, 'process', autospec=True) as (mock_nproc):
                    processor_mgr.map_method('process', self._make_data())
                    self.assertTrue(mock_cproc.called)
                    self.assertTrue(mock_pproc.called)
                    self.assertTrue(mock_nproc.called)