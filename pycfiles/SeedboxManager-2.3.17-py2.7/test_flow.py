# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-1.7.35-i686/egg/seedbox/tests/process/test_flow.py
# Compiled at: 2015-06-14 13:30:57
from seedbox import db
from seedbox.db import models
from seedbox.process import flow
from seedbox.tests import test

class FlowTestCase(test.ConfiguredBaseTestCase):

    def setUp(self):
        super(FlowTestCase, self).setUp()
        self.patch(db, '_DBAPI', {})
        self.dbapi = db.dbapi(self.CONF)
        self.torrent = self.dbapi.save_torrent(models.Torrent(torrent_id=None, name='fake1.torrent'))
        self.CONF.set_override('prepare', [
         'filecopy', 'fileunrar'], group='process')
        self.CONF.set_override('activate', [
         'filesync'], group='process')
        self.CONF.set_override('complete', [
         'filedelete'], group='process')
        return

    def test_base_flow(self):
        _medias = []
        _medias.append(models.MediaFile(media_id=None, torrent_id=self.torrent.torrent_id, filename='movie-1.mp4', file_ext='.mp4', file_path='/tmp/media/', compressed=0, synced=0, missing=0, skipped=0))
        _medias.append(models.MediaFile(media_id=None, torrent_id=self.torrent.torrent_id, filename='movie-2.rar', file_ext='.rar', file_path='/tmp/media/', compressed=1, synced=0, missing=0, skipped=0))
        self.dbapi.bulk_create_medias(_medias)
        wf = flow.BaseFlow(self.dbapi, self.torrent)
        tasks = wf.next_tasks()
        self.assertEqual(len(list(tasks)), 2)
        return