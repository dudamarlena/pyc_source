# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-2.2.1-i686/egg/tvrenamer/tests/cache/test_api.py
# Compiled at: 2015-11-08 18:31:47
import os, tempfile
from tvrenamer import cache
from tvrenamer.core import episode
from tvrenamer.tests import base

class SAApiTestCase(base.BaseTest):

    def setUp(self):
        super(SAApiTestCase, self).setUp()
        dbfile = os.path.join(tempfile.mkdtemp(), 'cache.json')
        self.CONF.set_override('dbfile', dbfile, 'cache')
        self.dbconn = cache.dbapi(self.CONF)

    def tearDown(self):
        cache._DBAPI = None
        super(SAApiTestCase, self).tearDown()
        return

    def test_clear(self):
        dbapi = cache.dbapi(self.CONF)
        dbapi.clear()
        self.assertTrue(True)

    def test_save(self):
        media = self.create_tempfiles([
         ('revenge.s04e12.hdtv.x264-2hd', 'dummy data')], '.mp4')[0]
        ep = episode.Episode(media)
        _saved_ep_id = self.dbconn.save(ep)
        self.assertIsInstance(_saved_ep_id, int)
        ep.formatted_filename = 'S04E12.mp4'
        _saved_ep_id = self.dbconn.save(ep)
        self.assertIsInstance(_saved_ep_id, int)