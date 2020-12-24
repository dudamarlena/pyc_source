# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/diffviewer/tests/test_diff_chunk_generator.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from reviewboard.diffviewer.chunk_generator import DiffChunkGenerator
from reviewboard.scmtools.core import PRE_CREATION
from reviewboard.testing import TestCase

class DiffChunkGeneratorTests(TestCase):
    """Unit tests for DiffChunkGenerator."""
    fixtures = [
     b'test_scmtools']

    def setUp(self):
        super(DiffChunkGeneratorTests, self).setUp()
        self.repository = self.create_repository()
        self.diffset = self.create_diffset(repository=self.repository)
        self.filediff = self.create_filediff(diffset=self.diffset)
        self.generator = DiffChunkGenerator(None, self.filediff)
        return

    def test_get_chunks_with_empty_added_file(self):
        """Testing DiffChunkGenerator.get_chunks with empty added file"""
        self.filediff.source_revision = PRE_CREATION
        self.filediff.extra_data.update({b'raw_insert_count': 0, 
           b'raw_delete_count': 0})
        self.assertEqual(len(list(self.generator.get_chunks())), 0)

    def test_get_chunks_with_replace_in_added_file_with_parent_diff(self):
        """Testing DiffChunkGenerator.get_chunks with replace chunks in
        added file with parent diff
        """
        self.filediff.diff = b'--- README\n+++ README\n@@ -1,1 +1,1 @@\n-line\n+line.\n'
        self.filediff.parent_diff = b'--- README\n+++ README\n@@ -0,0 +1,1 @@\n+line\n'
        self.filediff.source_revision = PRE_CREATION
        self.filediff.extra_data.update({b'raw_insert_count': 1, 
           b'raw_delete_count': 1, 
           b'insert_count': 0, 
           b'delete_count': 0})
        self.assertEqual(len(list(self.generator.get_chunks())), 1)

    def test_line_counts_unmodified_by_interdiff(self):
        """Testing that line counts are not modified by interdiffs where the
        changes are reverted
        """
        self.filediff.source_revision = PRE_CREATION
        self.filediff.diff = b'--- README\n+++ README\n@@ -0,0 +1,1 @@\n+line\n'
        self.assertEqual(len(list(self.generator.get_chunks())), 1)
        line_counts = self.filediff.get_line_counts()
        interdiff_generator = DiffChunkGenerator(request=None, filediff=self.filediff, interfilediff=None, force_interdiff=True)
        self.assertEqual(len(list(interdiff_generator.get_chunks())), 1)
        self.assertEqual(line_counts, self.filediff.get_line_counts())
        return