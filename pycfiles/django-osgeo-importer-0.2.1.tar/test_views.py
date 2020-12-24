# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /vagrant/osgeo_importer/test_views.py
# Compiled at: 2016-09-29 16:34:19
from django.test import TestCase
from osgeo_importer import views
from osgeo_importer import models

class TestFileAddView_upload(TestCase):
    """Test the helper method FileAddView.upload.
    """

    class FakeRequest(object):
        """Fake the kind of request object used by FileAddView.upload.
        """

        def __init__(self, user):
            self.user = user

    class FakeFile(object):
        """Fake the kind of file object used by FileAddView.upload.
        """

        def __init__(self, name):
            self.name = name

    def view(self):
        view = views.FileAddView()
        view.get_file_type = lambda path: 'BogusType'
        user = None
        view.request = self.FakeRequest(user)
        return view

    def test_empty(self):
        """Empty data should return None.

        Form validation should guard against this sort of argument coming to
        upload(), but if it does happen, upload() should behave reasonably.
        """
        data = []
        view = self.view()
        upload = view.upload(data)
        self.assertEqual(upload.name, None)
        self.assertEqual(upload.file_type, None)
        return

    def test_single(self):
        data = [
         self.FakeFile('/tmp/xyz/abc/foo.shp')]
        view = self.view()
        upload = view.upload(data)
        self.assertEqual(upload.name, 'foo.shp')
        self.assertEqual(upload.file_type, 'BogusType')

    def test_double(self):
        data = [
         self.FakeFile('/tmp/xyz/abc/foo.shp'),
         self.FakeFile('/tmp/xyz/abc/bar.shp')]
        view = self.view()
        upload = view.upload(data)
        self.assertEqual(upload.name, 'bar.shp, foo.shp')
        self.assertEqual(upload.file_type, None)
        return

    def test_single_too_long(self):
        max_length = models.UploadedData._meta.get_field('name').max_length
        too_long = 'ObviouslyWayWayWayWayWayWayWayWayWayWayWayWayWayWayTooLong'
        self.assertGreater(too_long, max_length)
        data = [
         self.FakeFile(('/tmp/{0}').format(too_long))]
        view = self.view()
        upload = view.upload(data)
        self.assertEqual(upload.name.startswith('Obviously'), True)
        self.assertEqual(upload.file_type, 'BogusType')

    def test_many_too_long(self):
        data = [
         self.FakeFile('/tmp/xyz/abc/NotTooLongOnItsOwn.shp'),
         self.FakeFile('/tmp/xyz/abc/rather_long_to_be_combined_with.shp'),
         self.FakeFile('/tmp/really_too_much.shp')]
        view = self.view()
        upload = view.upload(data)
        self.assertEqual(upload.name, None)
        self.assertEqual(upload.file_type, None)
        return