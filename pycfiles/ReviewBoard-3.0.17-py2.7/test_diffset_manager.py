# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/diffviewer/tests/test_diffset_manager.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from kgb import SpyAgency
from reviewboard.diffviewer.models import DiffSet, FileDiff
from reviewboard.testing import TestCase

class DiffSetManagerTests(SpyAgency, TestCase):
    """Unit tests for DiffSetManager."""
    fixtures = [
     b'test_scmtools']

    def test_create_from_data(self):
        """Testing DiffSetManager.create_from_data"""
        repository = self.create_repository(tool_name=b'Test')
        self.spy_on(repository.get_file_exists, call_fake=lambda *args, **kwargs: True)
        diffset = DiffSet.objects.create_from_data(repository=repository, diff_file_name=b'diff', diff_file_contents=self.DEFAULT_GIT_FILEDIFF_DATA, basedir=b'/')
        self.assertEqual(diffset.files.count(), 1)

    def test_create_from_data_with_basedir_no_slash(self):
        """Testing DiffSetManager.create_from_data with basedir without leading
        slash
        """
        repository = self.create_repository(tool_name=b'Test')
        self.spy_on(repository.get_file_exists, call_fake=lambda *args, **kwargs: True)
        diffset = DiffSet.objects.create_from_data(repository=repository, diff_file_name=b'diff', diff_file_contents=self.DEFAULT_GIT_FILEDIFF_DATA, basedir=b'trunk/')
        self.assertEqual(diffset.files.count(), 1)
        filediff = diffset.files.all()[0]
        self.assertEqual(filediff.source_file, b'trunk/README')
        self.assertEqual(filediff.dest_file, b'trunk/README')

    def test_create_from_data_with_basedir_slash(self):
        """Testing DiffSetManager.create_from_data with basedir with leading
        slash
        """
        repository = self.create_repository(tool_name=b'Test')
        self.spy_on(repository.get_file_exists, call_fake=lambda *args, **kwargs: True)
        diffset = DiffSet.objects.create_from_data(repository=repository, diff_file_name=b'diff', diff_file_contents=self.DEFAULT_GIT_FILEDIFF_DATA, basedir=b'/trunk/')
        self.assertEqual(diffset.files.count(), 1)
        filediff = diffset.files.all()[0]
        self.assertEqual(filediff.source_file, b'trunk/README')
        self.assertEqual(filediff.dest_file, b'trunk/README')

    def test_create_from_data_with_validate_only_true(self):
        """Testing DiffSetManager.create_from_data with validate_only=True"""
        repository = self.create_repository(tool_name=b'Test')
        self.spy_on(repository.get_file_exists, call_fake=lambda *args, **kwargs: True)
        with self.assertNumQueries(0):
            diffset = DiffSet.objects.create_from_data(repository=repository, diff_file_name=b'diff', diff_file_contents=self.DEFAULT_GIT_FILEDIFF_DATA, basedir=b'/', validate_only=True)
        self.assertIsNone(diffset)
        self.assertEqual(DiffSet.objects.count(), 0)
        self.assertEqual(FileDiff.objects.count(), 0)