# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/diffviewer/tests/test_filediff_migration.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from djblets.db.fields import Base64DecodedValue
from reviewboard.diffviewer.models import DiffSet, FileDiff, LegacyFileDiffData, RawFileDiffData
from reviewboard.testing import TestCase

class FileDiffMigrationTests(TestCase):
    """Unit tests for FileDiff migration."""
    fixtures = [
     b'test_scmtools']

    def setUp(self):
        super(FileDiffMigrationTests, self).setUp()
        self.repository = self.create_repository(tool_name=b'Test')
        diffset = DiffSet.objects.create(name=b'test', revision=1, repository=self.repository)
        self.filediff = FileDiff(source_file=b'README', dest_file=b'README', diffset=diffset, diff64=b'', parent_diff64=b'')
        self.parent_diff = b'diff --git a/README b/README\nindex 94bdd3e..3d2b777 100644\n--- README\n+++ README\n@@ -2 +2 @@\n-blah..\n+blah blah\n'
        repository = self.create_repository(tool_name=b'Test')
        diffset = DiffSet.objects.create(name=b'test', revision=1, repository=repository)
        self.filediff = FileDiff(source_file=b'README', dest_file=b'README', diffset=diffset, diff64=b'', parent_diff64=b'')

    def test_migration_by_diff(self):
        """Testing RawFileDiffData migration accessing FileDiff.diff"""
        self.filediff.diff64 = self.DEFAULT_GIT_FILEDIFF_DATA
        self.assertIsNone(self.filediff.diff_hash)
        self.assertIsNone(self.filediff.parent_diff_hash)
        diff = self.filediff.diff
        self.assertIsNone(self.filediff.parent_diff_hash)
        self.assertIsNotNone(self.filediff.diff_hash)
        self.assertEqual(diff, self.DEFAULT_GIT_FILEDIFF_DATA)
        self.assertEqual(self.filediff.diff64, b'')
        self.assertEqual(self.filediff.diff_hash.binary, self.DEFAULT_GIT_FILEDIFF_DATA)
        self.assertEqual(self.filediff.diff, diff)
        self.assertIsNone(self.filediff.parent_diff)
        self.assertIsNone(self.filediff.parent_diff_hash)

    def test_migration_by_parent_diff(self):
        """Testing RawFileDiffData migration accessing FileDiff.parent_diff"""
        self.filediff.diff64 = self.DEFAULT_GIT_FILEDIFF_DATA
        self.filediff.parent_diff64 = self.parent_diff
        self.assertIsNone(self.filediff.parent_diff_hash)
        parent_diff = self.filediff.parent_diff
        self.assertIsNotNone(self.filediff.parent_diff_hash)
        self.assertEqual(parent_diff, self.parent_diff)
        self.assertEqual(self.filediff.parent_diff64, b'')
        self.assertEqual(self.filediff.parent_diff_hash.binary, self.parent_diff)
        self.assertEqual(self.filediff.parent_diff, self.parent_diff)

    def test_migration_by_delete_count(self):
        """Testing RawFileDiffData migration accessing FileDiff.delete_count"""
        self.filediff.diff64 = self.DEFAULT_GIT_FILEDIFF_DATA
        self.assertIsNone(self.filediff.diff_hash)
        counts = self.filediff.get_line_counts()
        self.assertIsNotNone(self.filediff.diff_hash)
        self.assertEqual(counts[b'raw_delete_count'], 1)
        self.assertEqual(self.filediff.diff_hash.delete_count, 1)

    def test_migration_by_insert_count(self):
        """Testing RawFileDiffData migration accessing FileDiff.insert_count"""
        self.filediff.diff64 = self.DEFAULT_GIT_FILEDIFF_DATA
        self.assertIsNone(self.filediff.diff_hash)
        counts = self.filediff.get_line_counts()
        self.assertIsNotNone(self.filediff.diff_hash)
        self.assertEqual(counts[b'raw_insert_count'], 1)
        self.assertEqual(self.filediff.diff_hash.insert_count, 1)

    def test_migration_by_set_line_counts(self):
        """Testing RawFileDiffData migration calling FileDiff.set_line_counts
        """
        self.filediff.diff64 = self.DEFAULT_GIT_FILEDIFF_DATA
        self.assertIsNone(self.filediff.diff_hash)
        self.filediff.set_line_counts(raw_insert_count=10, raw_delete_count=20)
        self.assertIsNotNone(self.filediff.diff_hash)
        counts = self.filediff.get_line_counts()
        self.assertEqual(counts[b'raw_insert_count'], 10)
        self.assertEqual(counts[b'raw_delete_count'], 20)
        self.assertEqual(self.filediff.diff_hash.insert_count, 10)
        self.assertEqual(self.filediff.diff_hash.delete_count, 20)

    def test_migration_by_legacy_diff_hash(self):
        """Testing RawFileDiffData migration accessing FileDiff.diff
        with associated LegacyFileDiffData
        """
        legacy = LegacyFileDiffData.objects.create(binary_hash=b'abc123', binary=Base64DecodedValue(self.DEFAULT_GIT_FILEDIFF_DATA))
        self.filediff.legacy_diff_hash = legacy
        self.filediff.save()
        diff = self.filediff.diff
        self.assertIsNotNone(self.filediff.diff_hash)
        self.assertIsNone(self.filediff.parent_diff_hash)
        self.assertIsNone(self.filediff.legacy_diff_hash)
        self.assertEqual(LegacyFileDiffData.objects.count(), 0)
        self.assertEqual(diff, self.DEFAULT_GIT_FILEDIFF_DATA)
        self.assertEqual(self.filediff.diff64, b'')
        self.assertEqual(self.filediff.diff_hash.content, self.DEFAULT_GIT_FILEDIFF_DATA)
        self.assertEqual(self.filediff.diff, diff)
        self.assertIsNone(self.filediff.parent_diff)
        self.assertIsNone(self.filediff.parent_diff_hash)

    def test_migration_by_shared_legacy_diff_hash(self):
        """Testing RawFileDiffData migration accessing FileDiff.diff
        with associated shared LegacyFileDiffData
        """
        legacy = LegacyFileDiffData.objects.create(binary_hash=b'abc123', binary=Base64DecodedValue(self.DEFAULT_GIT_FILEDIFF_DATA))
        self.filediff.legacy_diff_hash = legacy
        self.filediff.save()
        diffset = DiffSet.objects.create(name=b'test', revision=1, repository=self.repository)
        FileDiff.objects.create(source_file=b'README', dest_file=b'README', diffset=diffset, diff64=b'', parent_diff64=b'', legacy_diff_hash=legacy)
        diff = self.filediff.diff
        self.assertIsNotNone(self.filediff.diff_hash)
        self.assertIsNone(self.filediff.parent_diff_hash)
        self.assertIsNone(self.filediff.legacy_diff_hash)
        self.assertEqual(LegacyFileDiffData.objects.count(), 1)
        self.assertEqual(diff, self.DEFAULT_GIT_FILEDIFF_DATA)
        self.assertEqual(self.filediff.diff64, b'')
        self.assertEqual(self.filediff.diff_hash.content, self.DEFAULT_GIT_FILEDIFF_DATA)
        self.assertEqual(self.filediff.diff, diff)
        self.assertIsNone(self.filediff.parent_diff)
        self.assertIsNone(self.filediff.parent_diff_hash)

    def test_migration_by_legacy_parent_diff_hash(self):
        """Testing RawFileDiffData migration accessing FileDiff.parent_diff
        with associated LegacyFileDiffData
        """
        legacy = LegacyFileDiffData.objects.create(binary_hash=b'abc123', binary=Base64DecodedValue(self.parent_diff))
        self.filediff.legacy_parent_diff_hash = legacy
        self.filediff.save()
        parent_diff = self.filediff.parent_diff
        self.assertIsNotNone(self.filediff.parent_diff_hash)
        self.assertIsNone(self.filediff.legacy_parent_diff_hash)
        self.assertEqual(parent_diff, self.parent_diff)
        self.assertEqual(self.filediff.parent_diff64, b'')
        self.assertEqual(self.filediff.parent_diff_hash.content, self.parent_diff)
        self.assertEqual(self.filediff.parent_diff, parent_diff)

    def test_migration_by_shared_legacy_parent_diff_hash(self):
        """Testing RawFileDiffData migration accessing FileDiff.parent_diff
        with associated shared LegacyFileDiffData
        """
        legacy = LegacyFileDiffData.objects.create(binary_hash=b'abc123', binary=Base64DecodedValue(self.parent_diff))
        self.filediff.legacy_parent_diff_hash = legacy
        self.filediff.save()
        diffset = DiffSet.objects.create(name=b'test', revision=1, repository=self.repository)
        FileDiff.objects.create(source_file=b'README', dest_file=b'README', diffset=diffset, diff64=b'', parent_diff64=b'', legacy_parent_diff_hash=legacy)
        parent_diff = self.filediff.parent_diff
        self.assertIsNotNone(self.filediff.parent_diff_hash)
        self.assertIsNone(self.filediff.legacy_parent_diff_hash)
        self.assertEqual(LegacyFileDiffData.objects.count(), 1)
        self.assertEqual(parent_diff, self.parent_diff)
        self.assertEqual(self.filediff.parent_diff64, b'')
        self.assertEqual(self.filediff.parent_diff_hash.content, self.parent_diff)
        self.assertEqual(self.filediff.parent_diff, parent_diff)

    def test_migration_with_legacy_and_race_condition(self):
        """Testing RawFileDiffData migration with LegacyFileDiffData and race
        condition in migrating
        """
        legacy = LegacyFileDiffData.objects.create(binary_hash=b'abc123', binary=Base64DecodedValue(self.DEFAULT_GIT_FILEDIFF_DATA))
        parent_legacy = LegacyFileDiffData.objects.create(binary_hash=b'def456', binary=Base64DecodedValue(self.parent_diff))
        filediff1 = self.filediff
        filediff1.legacy_diff_hash = legacy
        filediff1.legacy_parent_diff_hash = parent_legacy
        filediff1.save()
        filediff2 = FileDiff.objects.get(pk=filediff1.pk)
        self.assertEqual(filediff1.legacy_diff_hash_id, legacy.pk)
        self.assertEqual(filediff1.legacy_parent_diff_hash_id, parent_legacy.pk)
        self.assertEqual(filediff2.legacy_diff_hash_id, legacy.pk)
        self.assertEqual(filediff2.legacy_parent_diff_hash_id, parent_legacy.pk)
        diff1 = self.filediff.diff
        parent_diff1 = filediff1.parent_diff
        diff2 = filediff2.diff
        parent_diff2 = filediff2.parent_diff
        self.assertEqual(diff1, self.DEFAULT_GIT_FILEDIFF_DATA)
        self.assertEqual(diff1, diff2)
        self.assertEqual(parent_diff1, self.parent_diff)
        self.assertEqual(parent_diff1, parent_diff2)
        self.assertEqual(LegacyFileDiffData.objects.count(), 0)
        self.assertEqual(RawFileDiffData.objects.count(), 2)
        self.assertIsNotNone(filediff1.diff_hash)
        self.assertIsNotNone(filediff2.diff_hash)
        self.assertEqual(filediff1.diff_hash, filediff2.diff_hash)
        self.assertIsNotNone(filediff1.parent_diff_hash)
        self.assertIsNotNone(filediff2.parent_diff_hash)
        self.assertEqual(filediff1.parent_diff_hash, filediff2.parent_diff_hash)
        self.assertIsNone(filediff1.legacy_diff_hash)
        self.assertIsNone(filediff2.legacy_diff_hash)
        self.assertIsNone(filediff1.legacy_parent_diff_hash)
        self.assertIsNone(filediff2.legacy_parent_diff_hash)
        self.assertEqual(filediff1.diff64, b'')
        self.assertEqual(filediff2.diff64, b'')
        self.assertEqual(filediff1.diff_hash.content, self.DEFAULT_GIT_FILEDIFF_DATA)
        self.assertEqual(filediff2.diff_hash.content, self.DEFAULT_GIT_FILEDIFF_DATA)
        self.assertEqual(filediff1.parent_diff64, b'')
        self.assertEqual(filediff2.parent_diff64, b'')
        self.assertEqual(filediff1.parent_diff_hash.content, self.parent_diff)
        self.assertEqual(filediff2.parent_diff_hash.content, self.parent_diff)