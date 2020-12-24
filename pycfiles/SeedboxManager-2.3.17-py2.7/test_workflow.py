# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-1.7.35-i686/egg/seedbox/tests/process/test_workflow.py
# Compiled at: 2015-06-14 13:30:57
from seedbox import db
from seedbox.db import models
from seedbox.process import workflow
from seedbox.tests import test

class WorkflowTestCase(test.ConfiguredBaseTestCase):

    def setUp(self):
        super(WorkflowTestCase, self).setUp()
        self.patch(db, '_DBAPI', {})
        self.dbapi = db.dbapi(self.CONF)
        self.torrent = self.dbapi.save_torrent(models.Torrent(torrent_id=None, name='fake1.torrent'))
        return

    def test_workflow(self):
        wf = workflow.Workflow(self.dbapi, self.torrent)
        status = wf.run()
        self.assertFalse(status)
        status = wf.run()
        self.assertFalse(status)
        status = wf.run()
        self.assertTrue(status)
        status = wf.run()
        self.assertTrue(status)

    def test_cancelled(self):
        self.torrent.state = 'cancelled'
        wf = workflow.Workflow(self.dbapi, self.torrent)
        status = wf.run()
        self.assertTrue(status)

    def test_stop_workflow(self):
        torrent = self.dbapi.save_torrent(models.Torrent(torrent_id=None, name='fake177.torrent', state='active'))
        media = models.MediaFile(media_id=None, torrent_id=torrent.torrent_id, filename='movie-177.mp4', file_ext='.mp4', file_path='/tmp/media', error_msg='bad thing happened')
        media = self.dbapi.save_media(media)
        wf = workflow.Workflow(self.dbapi, torrent)
        status = wf.run()
        self.assertTrue(status)
        return