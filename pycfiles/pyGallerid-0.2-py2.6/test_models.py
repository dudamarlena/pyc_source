# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyGallerid/tests/test_models.py
# Compiled at: 2012-01-31 10:41:10
"""
Provides tests for the models of pyGallerid.
"""
import unittest, transaction
from pyramid import testing
from ..models import appmaker
from ..models.user import User
from ..models.gallery import Gallery, GalleryContainer, GalleryAlbum, GalleryPicture

class ViewTests(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()

    def tearDown(self):
        testing.tearDown()

    def test_my_view(self):
        from .views import my_view
        request = testing.DummyRequest()
        info = my_view(request)
        self.assertEqual(info['project'], 'gallery')


class ModelTests(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp()
        from sqlalchemy import create_engine
        from sqlalchemy.orm import sessionmaker
        engine = create_engine('sqlite:///:memory:')
        DBSession.configure(bind=engine)
        from zope.sqlalchemy import ZopeTransactionExtension
        Base.metadata.create_all(engine)
        with transaction.manager:
            from ..scripts.populate import test_fillDB
            test_fillDB(DBSession())

    def tearDown(self):
        DBSession.remove()
        testing.tearDown()

    def test_UserModel(self):
        pass

    def test_AlbumModel(self):
        pass

    def test_PictureModel(self):
        pass


def run():
    unittest.main()


if __name__ == '__main__':
    run()