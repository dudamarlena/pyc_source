# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-1.7.35-i686/egg/seedbox/tests/db/sqlalchemy/test_model_util.py
# Compiled at: 2015-06-14 13:30:57
from seedbox.db import models as api_model
from seedbox.db.sqlalchemy import model_util
from seedbox.db.sqlalchemy import models as db_model
from seedbox.db.sqlalchemy import session
from seedbox.tests import test

class ModelUtilTestCase(test.BaseTestCase):

    def setUp(self):
        super(ModelUtilTestCase, self).setUp()
        self.facade = session.EngineFacade('sqlite:///:memory:')
        db_model.verify_tables(self.facade.engine)

    def tearDown(self):
        db_model.purge_all_tables(self.facade.engine)
        super(ModelUtilTestCase, self).tearDown()

    def test_from_db(self):
        self.assertIsNone(model_util.from_db(None))
        _tor = db_model.Torrent()
        _tor['name'] = 'fake.torrent'
        _pub_tor = model_util.from_db(_tor)
        self.assertIsInstance(_pub_tor, api_model.Torrent)
        _mf = db_model.MediaFile()
        _mf['filename'] = 'media.mp4'
        _mf['file_ext'] = '.mp4'
        _mf['torrent_id'] = _tor.id
        _pub_mf = model_util.from_db(_mf)
        self.assertIsInstance(_pub_mf, api_model.MediaFile)
        return

    def test_to_db(self):
        self.assertIsNone(model_util.to_db(None))
        _tor = api_model.Torrent.make_empty()
        _tor.torrent_id = 1
        _tor.name = 'fake.torrent'
        _db_tor = model_util.to_db(_tor)
        self.assertIsInstance(_db_tor, db_model.Torrent)
        _mf = api_model.MediaFile.make_empty()
        _mf.media_id = 1
        _mf.filename = 'media.mp4'
        _mf.file_ext = '.mp4'
        _mf.torrent_id = _tor.torrent_id
        _tor.media_files = [
         _mf]
        _db_tor = model_util.to_db(_tor)
        self.assertIsInstance(_db_tor, db_model.Torrent)
        return