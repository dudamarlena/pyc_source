# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/diffviewer/tests/test_diffutils.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from django.test.client import RequestFactory
from django.utils.six.moves import zip_longest
from djblets.siteconfig.models import SiteConfiguration
from djblets.testing.decorators import add_fixtures
from kgb import SpyAgency
from reviewboard.diffviewer.diffutils import get_diff_files, get_displayed_diff_line_ranges, get_file_chunks_in_range, get_last_header_before_line, get_last_line_number_in_diff, get_line_changed_regions, get_matched_interdiff_files, get_original_file, patch, _PATCH_GARBAGE_INPUT, _get_last_header_in_chunks_before_line
from reviewboard.diffviewer.errors import PatchError
from reviewboard.diffviewer.models import FileDiff
from reviewboard.scmtools.core import PRE_CREATION
from reviewboard.testing import TestCase

class GetDiffFilesTests(TestCase):
    """Unit tests for get_diff_files."""

    @add_fixtures([b'test_users', b'test_scmtools'])
    def test_interdiff_when_renaming_twice(self):
        """Testing get_diff_files with interdiff when renaming twice"""
        repository = self.create_repository(tool_name=b'Git')
        review_request = self.create_review_request(repository=repository)
        one_to_two = b'diff --git a/foo.txt b/foo.txt\ndeleted file mode 100644\nindex 092beec..0000000\n--- a/foo.txt\n+++ /dev/null\n@@ -1,2 +0,0 @@\n-This is foo!\n-=]\ndiff --git a/foo2.txt b/foo2.txt\nnew file mode 100644\nindex 0000000..092beec\n--- /dev/null\n+++ b/foo2.txt\n@@ -0,0 +1,2 @@\n+This is foo!\n+=]\n'
        one_to_three = b'diff --git a/foo.txt b/foo.txt\ndeleted file mode 100644\nindex 092beec..0000000\n--- a/foo.txt\n+++ /dev/null\n@@ -1,2 +0,0 @@\n-This is foo!\n-=]\ndiff --git a/foo3.txt b/foo3.txt\nnew file mode 100644\nindex 0000000..092beec\n--- /dev/null\n+++ b/foo3.txt\n@@ -0,0 +1,2 @@\n+This is foo!\n+=]\n'
        diffset = self.create_diffset(review_request=review_request)
        self.create_filediff(diffset=diffset, source_file=b'foo.txt', dest_file=b'foo2.txt', status=FileDiff.MODIFIED, diff=one_to_two)
        interdiffset = self.create_diffset(review_request=review_request)
        self.create_filediff(diffset=interdiffset, source_file=b'foo.txt', dest_file=b'foo3.txt', status=FileDiff.MODIFIED, diff=one_to_three)
        diff_files = get_diff_files(diffset=diffset, interdiffset=interdiffset)
        two_to_three = diff_files[0]
        self.assertEqual(two_to_three[b'depot_filename'], b'foo2.txt')
        self.assertEqual(two_to_three[b'dest_filename'], b'foo3.txt')

    @add_fixtures([b'test_users', b'test_scmtools'])
    def test_get_diff_files_with_interdiff_and_files_same_source(self):
        """Testing get_diff_files with interdiff and multiple files using the
        same source_file
        """
        repository = self.create_repository(tool_name=b'Git')
        review_request = self.create_review_request(repository=repository)
        diffset = self.create_diffset(review_request=review_request, revision=1)
        filediff1 = self.create_filediff(diffset=diffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo.txt', dest_detail=b'124', diff=b'diff1')
        filediff2 = self.create_filediff(diffset=diffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo2.txt', dest_detail=b'124', status=FileDiff.COPIED, diff=b'diff2')
        filediff3 = self.create_filediff(diffset=diffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo3.txt', dest_detail=b'124', status=FileDiff.COPIED, diff=b'diff3')
        filediff4 = self.create_filediff(diffset=diffset, source_file=b'foo4.txt', source_revision=123, dest_file=b'foo4.txt', dest_detail=b'124', diff=b'diff4')
        interdiffset = self.create_diffset(review_request=review_request, revision=2)
        interfilediff1 = self.create_filediff(diffset=interdiffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo2.txt', dest_detail=b'124', status=FileDiff.COPIED, diff=b'interdiff1')
        interfilediff2 = self.create_filediff(diffset=interdiffset, source_file=b'foo.txt', source_revision=PRE_CREATION, dest_file=b'foo.txt', dest_detail=b'125', diff=b'interdiff2')
        interfilediff3 = self.create_filediff(diffset=interdiffset, source_file=b'foo4.txt', source_revision=123, dest_file=b'foo5.txt', dest_detail=b'124', diff=b'interdiff2')
        interfilediff4 = self.create_filediff(diffset=interdiffset, source_file=b'foo4.txt', source_revision=123, dest_file=b'foo6.txt', dest_detail=b'124', diff=b'interdiff3')
        diff_files = get_diff_files(diffset=diffset, interdiffset=interdiffset)
        self.assertEqual(len(diff_files), 6)
        diff_file = diff_files[0]
        self.assertEqual(diff_file[b'depot_filename'], b'foo.txt')
        self.assertEqual(diff_file[b'dest_filename'], b'foo.txt')
        self.assertEqual(diff_file[b'filediff'], filediff1)
        self.assertEqual(diff_file[b'interfilediff'], None)
        self.assertEqual(diff_file[b'revision'], b'Diff Revision 1')
        self.assertEqual(diff_file[b'dest_revision'], b'Diff Revision 2 - File Reverted')
        self.assertFalse(diff_file[b'is_new_file'])
        self.assertTrue(diff_file[b'force_interdiff'])
        diff_file = diff_files[1]
        self.assertEqual(diff_file[b'depot_filename'], b'foo.txt')
        self.assertEqual(diff_file[b'dest_filename'], b'foo.txt')
        self.assertEqual(diff_file[b'filediff'], interfilediff2)
        self.assertEqual(diff_file[b'interfilediff'], None)
        self.assertEqual(diff_file[b'revision'], b'Diff Revision 1')
        self.assertEqual(diff_file[b'dest_revision'], b'New File')
        self.assertTrue(diff_file[b'is_new_file'])
        self.assertFalse(diff_file[b'force_interdiff'])
        diff_file = diff_files[2]
        self.assertEqual(diff_file[b'depot_filename'], b'foo2.txt')
        self.assertEqual(diff_file[b'dest_filename'], b'foo2.txt')
        self.assertEqual(diff_file[b'filediff'], filediff2)
        self.assertEqual(diff_file[b'interfilediff'], interfilediff1)
        self.assertEqual(diff_file[b'revision'], b'Diff Revision 1')
        self.assertEqual(diff_file[b'dest_revision'], b'Diff Revision 2')
        self.assertFalse(diff_file[b'is_new_file'])
        self.assertTrue(diff_file[b'force_interdiff'])
        diff_file = diff_files[3]
        self.assertEqual(diff_file[b'depot_filename'], b'foo.txt')
        self.assertEqual(diff_file[b'dest_filename'], b'foo3.txt')
        self.assertEqual(diff_file[b'filediff'], filediff3)
        self.assertEqual(diff_file[b'interfilediff'], None)
        self.assertEqual(diff_file[b'revision'], b'Diff Revision 1')
        self.assertEqual(diff_file[b'dest_revision'], b'Diff Revision 2 - File Reverted')
        self.assertFalse(diff_file[b'is_new_file'])
        self.assertTrue(diff_file[b'force_interdiff'])
        diff_file = diff_files[4]
        self.assertEqual(diff_file[b'depot_filename'], b'foo4.txt')
        self.assertEqual(diff_file[b'dest_filename'], b'foo5.txt')
        self.assertEqual(diff_file[b'filediff'], filediff4)
        self.assertEqual(diff_file[b'interfilediff'], interfilediff3)
        self.assertEqual(diff_file[b'revision'], b'Diff Revision 1')
        self.assertEqual(diff_file[b'dest_revision'], b'Diff Revision 2')
        self.assertFalse(diff_file[b'is_new_file'])
        self.assertTrue(diff_file[b'force_interdiff'])
        diff_file = diff_files[5]
        self.assertEqual(diff_file[b'depot_filename'], b'foo4.txt')
        self.assertEqual(diff_file[b'dest_filename'], b'foo6.txt')
        self.assertEqual(diff_file[b'filediff'], filediff4)
        self.assertEqual(diff_file[b'interfilediff'], interfilediff4)
        self.assertEqual(diff_file[b'revision'], b'Diff Revision 1')
        self.assertEqual(diff_file[b'dest_revision'], b'Diff Revision 2')
        self.assertFalse(diff_file[b'is_new_file'])
        self.assertTrue(diff_file[b'force_interdiff'])
        return

    @add_fixtures([b'test_users', b'test_scmtools'])
    def test_get_diff_files_with_interdiff_using_filediff_only(self):
        """Testing get_diff_files with interdiff using filediff but no
        interfilediff
        """
        repository = self.create_repository(tool_name=b'Git')
        review_request = self.create_review_request(repository=repository)
        diffset = self.create_diffset(review_request=review_request, revision=1)
        filediff = self.create_filediff(diffset=diffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo.txt', diff=b'diff1')
        self.create_filediff(diffset=diffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo2.txt', status=FileDiff.COPIED, diff=b'diff2')
        interdiffset = self.create_diffset(review_request=review_request, revision=2)
        self.create_filediff(diffset=interdiffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo.txt', status=FileDiff.COPIED, diff=b'interdiff1')
        self.create_filediff(diffset=interdiffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo2.txt', status=FileDiff.COPIED, diff=b'interdiff2')
        diff_files = get_diff_files(diffset=diffset, interdiffset=interdiffset, filediff=filediff)
        self.assertEqual(len(diff_files), 1)
        diff_file = diff_files[0]
        self.assertEqual(diff_file[b'depot_filename'], b'foo.txt')
        self.assertEqual(diff_file[b'dest_filename'], b'foo.txt')
        self.assertEqual(diff_file[b'filediff'], filediff)
        self.assertEqual(diff_file[b'interfilediff'], None)
        self.assertEqual(diff_file[b'revision'], b'Diff Revision 1')
        self.assertEqual(diff_file[b'dest_revision'], b'Diff Revision 2 - File Reverted')
        self.assertFalse(diff_file[b'is_new_file'])
        self.assertTrue(diff_file[b'force_interdiff'])
        return

    @add_fixtures([b'test_users', b'test_scmtools'])
    def test_get_diff_files_with_interdiff_using_both_filediffs(self):
        """Testing get_diff_files with interdiff using filediff and
        interfilediff
        """
        repository = self.create_repository(tool_name=b'Git')
        review_request = self.create_review_request(repository=repository)
        diffset = self.create_diffset(review_request=review_request, revision=1)
        filediff = self.create_filediff(diffset=diffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo.txt', diff=b'diff1')
        self.create_filediff(diffset=diffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo2.txt', status=FileDiff.COPIED, diff=b'diff2')
        interdiffset = self.create_diffset(review_request=review_request, revision=2)
        interfilediff = self.create_filediff(diffset=interdiffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo.txt', status=FileDiff.COPIED, diff=b'interdiff1')
        self.create_filediff(diffset=interdiffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo2.txt', status=FileDiff.COPIED, diff=b'interdiff2')
        diff_files = get_diff_files(diffset=diffset, interdiffset=interdiffset, filediff=filediff, interfilediff=interfilediff)
        self.assertEqual(len(diff_files), 1)
        diff_file = diff_files[0]
        self.assertEqual(diff_file[b'depot_filename'], b'foo.txt')
        self.assertEqual(diff_file[b'dest_filename'], b'foo.txt')
        self.assertEqual(diff_file[b'filediff'], filediff)
        self.assertEqual(diff_file[b'interfilediff'], interfilediff)
        self.assertEqual(diff_file[b'revision'], b'Diff Revision 1')
        self.assertEqual(diff_file[b'dest_revision'], b'Diff Revision 2')
        self.assertFalse(diff_file[b'is_new_file'])
        self.assertTrue(diff_file[b'force_interdiff'])


class GetMatchedInterdiffFilesTests(TestCase):
    """Unit tests for get_matched_interdiff_files."""

    @add_fixtures([b'test_users', b'test_scmtools'])
    def test_with_simple_matches(self):
        """Testing get_matched_interdiff_files with simple source file matches
        """
        repository = self.create_repository(tool_name=b'Git')
        review_request = self.create_review_request(repository=repository)
        diffset = self.create_diffset(review_request=review_request, revision=1)
        filediff1 = self.create_filediff(diffset=diffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo.txt', diff=b'diff1')
        filediff2 = self.create_filediff(diffset=diffset, source_file=b'foo2.txt', source_revision=123, dest_file=b'foo2.txt', diff=b'diff2')
        interdiffset = self.create_diffset(review_request=review_request, revision=2)
        interfilediff1 = self.create_filediff(diffset=interdiffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo.txt', diff=b'interdiff1')
        interfilediff2 = self.create_filediff(diffset=interdiffset, source_file=b'foo2.txt', source_revision=123, dest_file=b'foo2.txt', diff=b'interdiff2')
        matched_files = get_matched_interdiff_files(tool=repository.get_scmtool(), filediffs=[
         filediff1, filediff2], interfilediffs=[
         interfilediff1, interfilediff2])
        self.assertEqual(list(matched_files), [
         (
          filediff1, interfilediff1),
         (
          filediff2, interfilediff2)])

    @add_fixtures([b'test_users', b'test_scmtools'])
    def test_with_new_added_file_left(self):
        """Testing get_matched_interdiff_files with new added file on left
        side only
        """
        repository = self.create_repository(tool_name=b'Git')
        review_request = self.create_review_request(repository=repository)
        diffset = self.create_diffset(review_request=review_request, revision=1)
        filediff1 = self.create_filediff(diffset=diffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo.txt', diff=b'diff1')
        filediff2 = self.create_filediff(diffset=diffset, source_file=b'foo2.txt', source_revision=PRE_CREATION, dest_file=b'foo2.txt', diff=b'diff2')
        interdiffset = self.create_diffset(review_request=review_request, revision=2)
        interfilediff1 = self.create_filediff(diffset=interdiffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo.txt', diff=b'interdiff1')
        matched_files = get_matched_interdiff_files(tool=repository.get_scmtool(), filediffs=[
         filediff1, filediff2], interfilediffs=[
         interfilediff1])
        self.assertEqual(list(matched_files), [
         (
          filediff1, interfilediff1),
         (
          filediff2, None)])
        return

    @add_fixtures([b'test_users', b'test_scmtools'])
    def test_with_new_added_file_right(self):
        """Testing get_matched_interdiff_files with new added file on right
        side only
        """
        repository = self.create_repository(tool_name=b'Git')
        review_request = self.create_review_request(repository=repository)
        diffset = self.create_diffset(review_request=review_request, revision=1)
        filediff1 = self.create_filediff(diffset=diffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo.txt', diff=b'diff1')
        interdiffset = self.create_diffset(review_request=review_request, revision=2)
        interfilediff1 = self.create_filediff(diffset=interdiffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo.txt', diff=b'interdiff1')
        interfilediff2 = self.create_filediff(diffset=interdiffset, source_file=b'foo2.txt', source_revision=PRE_CREATION, dest_file=b'foo2.txt', diff=b'interdiff2')
        matched_files = get_matched_interdiff_files(tool=repository.get_scmtool(), filediffs=[
         filediff1], interfilediffs=[
         interfilediff1, interfilediff2])
        self.assertEqual(list(matched_files), [
         (
          filediff1, interfilediff1),
         (
          None, interfilediff2)])
        return

    @add_fixtures([b'test_users', b'test_scmtools'])
    def test_with_new_added_file_both(self):
        """Testing get_matched_interdiff_files with new added file on both
        sides
        """
        repository = self.create_repository(tool_name=b'Git')
        review_request = self.create_review_request(repository=repository)
        diffset = self.create_diffset(review_request=review_request, revision=1)
        filediff1 = self.create_filediff(diffset=diffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo.txt', diff=b'diff1')
        filediff2 = self.create_filediff(diffset=diffset, source_file=b'foo2.txt', source_revision=PRE_CREATION, dest_file=b'foo2.txt', diff=b'diff2')
        interdiffset = self.create_diffset(review_request=review_request, revision=2)
        interfilediff1 = self.create_filediff(diffset=interdiffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo.txt', diff=b'interdiff1')
        interfilediff2 = self.create_filediff(diffset=interdiffset, source_file=b'foo2.txt', source_revision=PRE_CREATION, dest_file=b'foo2.txt', diff=b'interdiff2')
        matched_files = get_matched_interdiff_files(tool=repository.get_scmtool(), filediffs=[
         filediff1, filediff2], interfilediffs=[
         interfilediff1, interfilediff2])
        self.assertEqual(list(matched_files), [
         (
          filediff1, interfilediff1),
         (
          filediff2, interfilediff2)])

    @add_fixtures([b'test_users', b'test_scmtools'])
    def test_with_new_deleted_file_left(self):
        """Testing get_matched_interdiff_files with new deleted file on left
        side only
        """
        repository = self.create_repository(tool_name=b'Git')
        review_request = self.create_review_request(repository=repository)
        diffset = self.create_diffset(review_request=review_request, revision=1)
        filediff1 = self.create_filediff(diffset=diffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo.txt', diff=b'diff1')
        filediff2 = self.create_filediff(diffset=diffset, source_file=b'foo2.txt', source_revision=123, dest_file=b'foo2.txt', status=FileDiff.DELETED, diff=b'diff2')
        interdiffset = self.create_diffset(review_request=review_request, revision=2)
        interfilediff1 = self.create_filediff(diffset=interdiffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo.txt', diff=b'interdiff1')
        matched_files = get_matched_interdiff_files(tool=repository.get_scmtool(), filediffs=[
         filediff1, filediff2], interfilediffs=[
         interfilediff1])
        self.assertEqual(list(matched_files), [
         (
          filediff1, interfilediff1),
         (
          filediff2, None)])
        return

    @add_fixtures([b'test_users', b'test_scmtools'])
    def test_with_new_deleted_file_right(self):
        """Testing get_matched_interdiff_files with new deleted file on right
        side only
        """
        repository = self.create_repository(tool_name=b'Git')
        review_request = self.create_review_request(repository=repository)
        diffset = self.create_diffset(review_request=review_request, revision=1)
        filediff1 = self.create_filediff(diffset=diffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo.txt', diff=b'diff1')
        interdiffset = self.create_diffset(review_request=review_request, revision=2)
        interfilediff1 = self.create_filediff(diffset=interdiffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo.txt', diff=b'interdiff1')
        interfilediff2 = self.create_filediff(diffset=interdiffset, source_file=b'foo2.txt', source_revision=123, dest_file=b'foo2.txt', status=FileDiff.DELETED, diff=b'interdiff2')
        matched_files = get_matched_interdiff_files(tool=repository.get_scmtool(), filediffs=[
         filediff1], interfilediffs=[
         interfilediff1, interfilediff2])
        self.assertEqual(list(matched_files), [
         (
          filediff1, interfilediff1),
         (
          None, interfilediff2)])
        return

    @add_fixtures([b'test_users', b'test_scmtools'])
    def test_with_new_deleted_file_both(self):
        """Testing get_matched_interdiff_files with new deleted file on both
        sides
        """
        repository = self.create_repository(tool_name=b'Git')
        review_request = self.create_review_request(repository=repository)
        diffset = self.create_diffset(review_request=review_request, revision=1)
        filediff1 = self.create_filediff(diffset=diffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo.txt', diff=b'diff1')
        filediff2 = self.create_filediff(diffset=diffset, source_file=b'foo2.txt', source_revision=123, dest_file=b'foo2.txt', status=FileDiff.DELETED, diff=b'diff2')
        interdiffset = self.create_diffset(review_request=review_request, revision=2)
        interfilediff1 = self.create_filediff(diffset=interdiffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo.txt', diff=b'interdiff1')
        interfilediff2 = self.create_filediff(diffset=interdiffset, source_file=b'foo2.txt', source_revision=123, dest_file=b'foo2.txt', status=FileDiff.DELETED, diff=b'interdiff2')
        matched_files = get_matched_interdiff_files(tool=repository.get_scmtool(), filediffs=[
         filediff1, filediff2], interfilediffs=[
         interfilediff1, interfilediff2])
        self.assertEqual(list(matched_files), [
         (
          filediff1, interfilediff1),
         (
          filediff2, interfilediff2)])

    @add_fixtures([b'test_users', b'test_scmtools'])
    def test_with_new_modified_file_right(self):
        """Testing get_matched_interdiff_files with new modified file on
        right side
        """
        repository = self.create_repository(tool_name=b'Git')
        review_request = self.create_review_request(repository=repository)
        diffset = self.create_diffset(review_request=review_request, revision=1)
        filediff1 = self.create_filediff(diffset=diffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo.txt', diff=b'diff1')
        interdiffset = self.create_diffset(review_request=review_request, revision=2)
        interfilediff1 = self.create_filediff(diffset=interdiffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo.txt', diff=b'interdiff1')
        interfilediff2 = self.create_filediff(diffset=interdiffset, source_file=b'foo2.txt', source_revision=123, dest_file=b'foo2.txt', diff=b'interdiff2')
        matched_files = get_matched_interdiff_files(tool=repository.get_scmtool(), filediffs=[
         filediff1], interfilediffs=[
         interfilediff1, interfilediff2])
        self.assertEqual(list(matched_files), [
         (
          filediff1, interfilediff1),
         (
          None, interfilediff2)])
        return

    @add_fixtures([b'test_users', b'test_scmtools'])
    def test_with_reverted_file(self):
        """Testing get_matched_interdiff_files with reverted file"""
        repository = self.create_repository(tool_name=b'Git')
        review_request = self.create_review_request(repository=repository)
        diffset = self.create_diffset(review_request=review_request, revision=1)
        filediff1 = self.create_filediff(diffset=diffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo.txt', diff=b'diff1')
        filediff2 = self.create_filediff(diffset=diffset, source_file=b'foo2.txt', source_revision=123, dest_file=b'foo2.txt', diff=b'diff2')
        interdiffset = self.create_diffset(review_request=review_request, revision=2)
        interfilediff1 = self.create_filediff(diffset=interdiffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo.txt', diff=b'interdiff1')
        matched_files = get_matched_interdiff_files(tool=repository.get_scmtool(), filediffs=[
         filediff1, filediff2], interfilediffs=[
         interfilediff1])
        self.assertEqual(list(matched_files), [
         (
          filediff1, interfilediff1),
         (
          filediff2, None)])
        return

    @add_fixtures([b'test_users', b'test_scmtools'])
    def test_with_both_renames(self):
        """Testing get_matched_interdiff_files with matching renames on both
        sides
        """
        repository = self.create_repository(tool_name=b'Git')
        review_request = self.create_review_request(repository=repository)
        diffset = self.create_diffset(review_request=review_request, revision=1)
        filediff1 = self.create_filediff(diffset=diffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo.txt', diff=b'diff1')
        filediff2 = self.create_filediff(diffset=diffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo2.txt', diff=b'diff2')
        interdiffset = self.create_diffset(review_request=review_request, revision=2)
        interfilediff1 = self.create_filediff(diffset=interdiffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo.txt', diff=b'interdiff1')
        interfilediff2 = self.create_filediff(diffset=interdiffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo2.txt', diff=b'interdiff2')
        matched_files = get_matched_interdiff_files(tool=repository.get_scmtool(), filediffs=[
         filediff1, filediff2], interfilediffs=[
         interfilediff1, interfilediff2])
        self.assertEqual(list(matched_files), [
         (
          filediff1, interfilediff1),
         (
          filediff2, interfilediff2)])

    @add_fixtures([b'test_users', b'test_scmtools'])
    def test_with_new_renames(self):
        """Testing get_matched_interdiff_files with modified on left side,
        modified + renamed on right
        """
        repository = self.create_repository(tool_name=b'Git')
        review_request = self.create_review_request(repository=repository)
        diffset = self.create_diffset(review_request=review_request, revision=1)
        filediff1 = self.create_filediff(diffset=diffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo.txt', diff=b'diff1')
        filediff2 = self.create_filediff(diffset=diffset, source_file=b'foo2.txt', source_revision=123, dest_file=b'foo2.txt', diff=b'diff2')
        interdiffset = self.create_diffset(review_request=review_request, revision=2)
        interfilediff1 = self.create_filediff(diffset=interdiffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo.txt', diff=b'interdiff1')
        interfilediff2 = self.create_filediff(diffset=interdiffset, source_file=b'foo2.txt', source_revision=123, dest_file=b'foo3.txt', diff=b'interdiff2')
        matched_files = get_matched_interdiff_files(tool=repository.get_scmtool(), filediffs=[
         filediff1, filediff2], interfilediffs=[
         interfilediff1, interfilediff2])
        self.assertEqual(list(matched_files), [
         (
          filediff1, interfilediff1),
         (
          filediff2, interfilediff2)])

    @add_fixtures([b'test_users', b'test_scmtools'])
    def test_with_multiple_copies(self):
        """Testing get_matched_interdiff_files with multiple copies of file
        from left on right
        """
        repository = self.create_repository(tool_name=b'Git')
        review_request = self.create_review_request(repository=repository)
        diffset = self.create_diffset(review_request=review_request, revision=1)
        filediff1 = self.create_filediff(diffset=diffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo.txt', diff=b'diff1')
        filediff2 = self.create_filediff(diffset=diffset, source_file=b'foo2.txt', source_revision=123, dest_file=b'foo2.txt', diff=b'diff2')
        interdiffset = self.create_diffset(review_request=review_request, revision=2)
        interfilediff1 = self.create_filediff(diffset=interdiffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo.txt', diff=b'interdiff1')
        interfilediff2 = self.create_filediff(diffset=interdiffset, source_file=b'foo2.txt', source_revision=123, dest_file=b'foo3.txt', diff=b'interdiff2')
        interfilediff3 = self.create_filediff(diffset=interdiffset, source_file=b'foo2.txt', source_revision=123, dest_file=b'foo4.txt', diff=b'interdiff3')
        matched_files = get_matched_interdiff_files(tool=repository.get_scmtool(), filediffs=[
         filediff1, filediff2], interfilediffs=[
         interfilediff1, interfilediff2, interfilediff3])
        self.assertEqual(list(matched_files), [
         (
          filediff1, interfilediff1),
         (
          filediff2, interfilediff2),
         (
          filediff2, interfilediff3)])

    @add_fixtures([b'test_users', b'test_scmtools'])
    def test_with_added_left_only(self):
        """Testing get_matched_interdiff_files with file added in left only"""
        repository = self.create_repository(tool_name=b'Git')
        review_request = self.create_review_request(repository=repository)
        diffset = self.create_diffset(review_request=review_request, revision=1)
        filediff1 = self.create_filediff(diffset=diffset, source_file=b'foo.txt', source_revision=PRE_CREATION, dest_file=b'foo.txt', dest_detail=b'124', diff=b'diff1')
        filediff2 = self.create_filediff(diffset=diffset, source_file=b'foo2.txt', source_revision=123, dest_file=b'foo2.txt', dest_detail=b'124', diff=b'diff2')
        interdiffset = self.create_diffset(review_request=review_request, revision=2)
        interfilediff1 = self.create_filediff(diffset=interdiffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo.txt', dest_detail=b'124', diff=b'interdiff1')
        interfilediff2 = self.create_filediff(diffset=interdiffset, source_file=b'foo2.txt', source_revision=PRE_CREATION, dest_file=b'foo3.txt', dest_detail=b'125', diff=b'interdiff2')
        matched_files = get_matched_interdiff_files(tool=repository.get_scmtool(), filediffs=[
         filediff1, filediff2], interfilediffs=[
         interfilediff1, interfilediff2])
        self.assertEqual(list(matched_files), [
         (
          filediff1, interfilediff1),
         (
          filediff2, None),
         (
          None, interfilediff2)])
        return

    @add_fixtures([b'test_users', b'test_scmtools'])
    def test_with_deleted_right_only(self):
        """Testing get_matched_interdiff_files with file deleted in right only
        """
        repository = self.create_repository(tool_name=b'Git')
        review_request = self.create_review_request(repository=repository)
        diffset = self.create_diffset(review_request=review_request, revision=1)
        filediff1 = self.create_filediff(diffset=diffset, source_file=b'foo.txt', source_revision=b'123', dest_file=b'foo.txt', diff=b'diff1')
        filediff2 = self.create_filediff(diffset=diffset, source_file=b'foo2.txt', source_revision=123, dest_file=b'foo2.txt', status=FileDiff.DELETED, diff=b'diff2')
        interdiffset = self.create_diffset(review_request=review_request, revision=2)
        interfilediff1 = self.create_filediff(diffset=interdiffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo.txt', status=FileDiff.DELETED, diff=b'interdiff1')
        interfilediff2 = self.create_filediff(diffset=interdiffset, source_file=b'foo2.txt', source_revision=123, dest_file=b'foo3.txt', diff=b'interdiff2')
        matched_files = get_matched_interdiff_files(tool=repository.get_scmtool(), filediffs=[
         filediff1, filediff2], interfilediffs=[
         interfilediff1, interfilediff2])
        self.assertEqual(list(matched_files), [
         (
          filediff1, interfilediff1),
         (
          filediff2, None),
         (
          None, interfilediff2)])
        return

    @add_fixtures([b'test_users', b'test_scmtools'])
    def test_with_same_names_multiple_ops(self):
        """Testing get_matched_interdiff_files with same names and multiple
        operation (pathological case)
        """
        repository = self.create_repository(tool_name=b'Git')
        review_request = self.create_review_request(repository=repository)
        diffset = self.create_diffset(review_request=review_request, revision=1)
        filediff1 = self.create_filediff(diffset=diffset, source_file=b'foo.txt', source_revision=PRE_CREATION, dest_file=b'foo.txt', diff=b'diff1')
        filediff2 = self.create_filediff(diffset=diffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo.txt', diff=b'diff2')
        filediff3 = self.create_filediff(diffset=diffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo2.txt', diff=b'diff3')
        filediff4 = self.create_filediff(diffset=diffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo.txt', status=FileDiff.DELETED, diff=b'diff1')
        interdiffset = self.create_diffset(review_request=review_request, revision=2)
        interfilediff1 = self.create_filediff(diffset=interdiffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo3.txt', diff=b'interdiff1')
        interfilediff2 = self.create_filediff(diffset=interdiffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo2.txt', diff=b'interdiff2')
        interfilediff3 = self.create_filediff(diffset=interdiffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo3.txt', diff=b'interdiff3')
        interfilediff4 = self.create_filediff(diffset=interdiffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo.txt', status=FileDiff.DELETED, diff=b'interdiff4')
        interfilediff5 = self.create_filediff(diffset=interdiffset, source_file=b'foo.txt', source_revision=PRE_CREATION, dest_file=b'foo.txt', diff=b'interdiff5')
        matched_files = get_matched_interdiff_files(tool=repository.get_scmtool(), filediffs=[
         filediff1, filediff2, filediff3, filediff4], interfilediffs=[
         interfilediff1, interfilediff2, interfilediff3,
         interfilediff4, interfilediff5])
        self.assertEqual(list(matched_files), [
         (
          filediff1, interfilediff5),
         (
          filediff3, interfilediff2),
         (
          filediff4, interfilediff4),
         (
          filediff2, interfilediff1),
         (
          filediff2, interfilediff3)])

    @add_fixtures([b'test_users', b'test_scmtools'])
    def test_with_new_file_same_name(self):
        """Testing get_matched_interdiff_files with new file on right with
        same name from left
        """
        repository = self.create_repository(tool_name=b'Git')
        review_request = self.create_review_request(repository=repository)
        diffset = self.create_diffset(review_request=review_request, revision=1)
        interdiffset = self.create_diffset(review_request=review_request, revision=2)
        filediff1 = self.create_filediff(diffset=diffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo.txt', dest_detail=b'124', diff=b'diff1')
        interfilediff1 = self.create_filediff(diffset=interdiffset, source_file=b'foo.txt', source_revision=123, dest_file=b'foo.txt', dest_detail=b'124', diff=b'interdiff1')
        filediff2 = self.create_filediff(diffset=diffset, source_file=b'foo2.txt', source_revision=123, dest_file=b'foo2.txt', dest_detail=b'124', diff=b'diff2')
        interfilediff2 = self.create_filediff(diffset=interdiffset, source_file=b'foo2.txt', source_revision=PRE_CREATION, dest_file=b'foo2.txt', dest_detail=b'124', diff=b'interdiff2')
        filediff3 = self.create_filediff(diffset=diffset, source_file=b'foo3.txt', source_revision=123, dest_file=b'foo3.txt', dest_detail=b'124', diff=b'diff3')
        interfilediff3 = self.create_filediff(diffset=interdiffset, source_file=b'foo3.txt', source_revision=PRE_CREATION, dest_file=b'foo3.txt', dest_detail=b'125', diff=b'interdiff3')
        matched_files = get_matched_interdiff_files(tool=repository.get_scmtool(), filediffs=[
         filediff1, filediff2, filediff3], interfilediffs=[
         interfilediff1, interfilediff2, interfilediff3])
        self.assertEqual(list(matched_files), [
         (
          filediff1, interfilediff1),
         (
          filediff2, interfilediff2),
         (
          filediff3, None),
         (
          None, interfilediff3)])
        return


class GetLineChangedRegionsTests(TestCase):
    """Unit tests for get_line_changed_regions."""

    def test_get_line_changed_regions(self):
        """Testing get_line_changed_regions"""

        def deep_equal(A, B):
            typea, typeb = type(A), type(B)
            self.assertEqual(typea, typeb)
            if typea is tuple or typea is list:
                for a, b in zip_longest(A, B):
                    deep_equal(a, b)

            else:
                self.assertEqual(A, B)

        deep_equal(get_line_changed_regions(None, None), (None, None))
        old = b'submitter = models.ForeignKey(Person, verbose_name="Submitter")'
        new = b'submitter = models.ForeignKey(User, verbose_name="Submitter")'
        regions = get_line_changed_regions(old, new)
        deep_equal(regions, ([(30, 36)], [(30, 34)]))
        old = b'-from reviews.models import ReviewRequest, Person, Group'
        new = b'+from .reviews.models import ReviewRequest, Group'
        regions = get_line_changed_regions(old, new)
        deep_equal(regions, ([(0, 1), (6, 6), (43, 51)],
         [
          (0, 1), (6, 7), (44, 44)]))
        old = b'abcdefghijklm'
        new = b'nopqrstuvwxyz'
        regions = get_line_changed_regions(old, new)
        deep_equal(regions, (None, None))
        return


class GetDisplayedDiffLineRangesTests(TestCase):
    """Unit tests for get_displayed_diff_line_ranges."""

    def test_with_delete_single_lines(self):
        """Testing get_displayed_diff_line_ranges with delete chunk and single
        virtual line
        """
        chunks = [
         {b'change': b'delete', 
            b'lines': [
                     (
                      10, 20, b'deleted line', [], b'', b'', [], False),
                     (
                      50, 60, b'deleted line', [], b'', b'', [], False)]}]
        self.assertEqual(get_displayed_diff_line_ranges(chunks, 20, 20), (
         {b'display_range': (30, 30), 
            b'virtual_range': (20, 20), 
            b'chunk_range': (
                           chunks[0], chunks[0])},
         None))
        return

    def test_with_delete_mutiple_lines(self):
        """Testing get_displayed_diff_line_ranges with delete chunk and multiple
        virtual lines
        """
        chunks = [
         {b'change': b'delete', 
            b'lines': [
                     (
                      10, 20, b'deleted line', [], b'', b'', [], False),
                     (
                      50, 60, b'deleted line', [], b'', b'', [], False)]}]
        self.assertEqual(get_displayed_diff_line_ranges(chunks, 20, 21), (
         {b'display_range': (30, 31), 
            b'virtual_range': (20, 21), 
            b'chunk_range': (
                           chunks[0], chunks[0])},
         None))
        return

    def test_with_replace_single_line(self):
        """Testing get_displayed_diff_line_ranges with replace chunk and single
        virtual line
        """
        chunks = [
         {b'change': b'replace', 
            b'lines': [
                     (
                      10, 20, b'foo', [], 30, b'replaced line', [], False),
                     (
                      50, 60, b'foo', [], 70, b'replaced line', [], False)]}]
        self.assertEqual(get_displayed_diff_line_ranges(chunks, 20, 20), (
         {b'display_range': (30, 30), 
            b'virtual_range': (20, 20), 
            b'chunk_range': (
                           chunks[0], chunks[0])},
         {b'display_range': (40, 40), 
            b'virtual_range': (20, 20), 
            b'chunk_range': (
                           chunks[0], chunks[0])}))

    def test_with_replace_multiple_lines(self):
        """Testing get_displayed_diff_line_ranges with replace chunk and
        multiple virtual lines
        """
        chunks = [
         {b'change': b'replace', 
            b'lines': [
                     (
                      10, 20, b'foo', [], 30, b'replaced line', [], False),
                     (
                      50, 60, b'foo', [], 70, b'replaced line', [], False)]}]
        self.assertEqual(get_displayed_diff_line_ranges(chunks, 20, 21), (
         {b'display_range': (30, 31), 
            b'virtual_range': (20, 21), 
            b'chunk_range': (
                           chunks[0], chunks[0])},
         {b'display_range': (40, 41), 
            b'virtual_range': (20, 21), 
            b'chunk_range': (
                           chunks[0], chunks[0])}))

    def test_with_insert_single_line(self):
        """Testing get_displayed_diff_line_ranges with insert chunk and single
        virtual line
        """
        chunks = [
         {b'change': b'insert', 
            b'lines': [
                     (
                      10, b'', b'', [], 20, b'inserted line', [], False),
                     (
                      50, b'', b'', [], 60, b'inserted line', [], False)]}]
        self.assertEqual(get_displayed_diff_line_ranges(chunks, 20, 20), (
         None,
         {b'display_range': (30, 30), 
            b'virtual_range': (20, 20), 
            b'chunk_range': (
                           chunks[0], chunks[0])}))
        return

    def test_with_insert_multiple_lines(self):
        """Testing get_displayed_diff_line_ranges with insert chunk and multiple
        virtual lines
        """
        chunks = [
         {b'change': b'insert', 
            b'lines': [
                     (
                      10, b'', b'', [], 20, b'inserted line', [], False),
                     (
                      50, b'', b'', [], 60, b'inserted line', [], False)]}]
        self.assertEqual(get_displayed_diff_line_ranges(chunks, 20, 21), (
         None,
         {b'display_range': (30, 31), 
            b'virtual_range': (20, 21), 
            b'chunk_range': (
                           chunks[0], chunks[0])}))
        return

    def test_with_fake_equal_orig(self):
        """Testing get_displayed_diff_line_ranges with fake equal from
        original side of interdiff
        """
        chunks = [
         {b'change': b'equal', 
            b'lines': [
                     (
                      10, b'', b'', [], 20, b'inserted line', [], False),
                     (
                      50, b'', b'', [], 60, b'inserted line', [], False)]}]
        self.assertEqual(get_displayed_diff_line_ranges(chunks, 20, 21), (
         None,
         {b'display_range': (30, 31), 
            b'virtual_range': (20, 21), 
            b'chunk_range': (
                           chunks[0], chunks[0])}))
        return

    def test_with_fake_equal_patched(self):
        """Testing get_displayed_diff_line_ranges with fake equal from
        patched side of interdiff
        """
        chunks = [
         {b'change': b'equal', 
            b'lines': [
                     (
                      10, 20, b'deleted line', [], b'', b'', [], False),
                     (
                      50, 60, b'deleted line', [], b'', b'', [], False)]}]
        self.assertEqual(get_displayed_diff_line_ranges(chunks, 20, 21), (
         {b'display_range': (30, 31), 
            b'virtual_range': (20, 21), 
            b'chunk_range': (
                           chunks[0], chunks[0])},
         None))
        return

    def test_with_spanning_insert_delete(self):
        """Testing get_displayed_diff_line_ranges with spanning delete and
        insert
        """
        chunks = [
         {b'change': b'delete', 
            b'lines': [
                     (
                      10, 20, b'deleted line', [], b'', b'', [], False),
                     (
                      50, 60, b'deleted line', [], b'', b'', [], False)]},
         {b'change': b'insert', 
            b'lines': [
                     (
                      51, b'', b'', [], 61, b'inserted line', [], False),
                     (
                      100, b'', b'', [], 110, b'inserted line', [], False)]},
         {b'change': b'equal', 
            b'lines': [
                     (
                      101, 61, b'equal line', [], 111, b'equal line', [],
                      False),
                     (
                      200, 160, b'equal line', [], 210, b'equal line', [],
                      False)]}]
        self.assertEqual(get_displayed_diff_line_ranges(chunks, 20, 69), (
         {b'display_range': (30, 60), 
            b'virtual_range': (20, 50), 
            b'chunk_range': (
                           chunks[0], chunks[0])},
         {b'display_range': (61, 79), 
            b'virtual_range': (51, 69), 
            b'chunk_range': (
                           chunks[1], chunks[1])}))

    def test_with_spanning_delete_insert(self):
        """Testing get_displayed_diff_line_ranges with spanning insert and
        delete
        """
        chunks = [
         {b'change': b'insert', 
            b'lines': [
                     (
                      10, b'', b'', [], 20, b'inserted line', [], False),
                     (
                      50, b'', b'', [], 60, b'inserted line', [], False)]},
         {b'change': b'delete', 
            b'lines': [
                     (
                      51, 61, b'inserted line', [], b'', b'', [], False),
                     (
                      100, 110, b'inserted line', [], b'', b'', [], False)]},
         {b'change': b'equal', 
            b'lines': [
                     (
                      101, 111, b'equal line', [], 61, b'equal line', [],
                      False),
                     (
                      200, 210, b'equal line', [], 160, b'equal line', [],
                      False)]}]
        self.assertEqual(get_displayed_diff_line_ranges(chunks, 20, 69), (
         {b'display_range': (61, 79), 
            b'virtual_range': (51, 69), 
            b'chunk_range': (
                           chunks[1], chunks[1])},
         {b'display_range': (30, 60), 
            b'virtual_range': (20, 50), 
            b'chunk_range': (
                           chunks[0], chunks[0])}))

    def test_with_spanning_last_chunk(self):
        """Testing get_displayed_diff_line_ranges with spanning chunks through
        last chunk
        """
        chunks = [
         {b'change': b'delete', 
            b'lines': [
                     (
                      10, 20, b'deleted line', [], b'', b'', [], False),
                     (
                      50, 60, b'deleted line', [], b'', b'', [], False)]},
         {b'change': b'insert', 
            b'lines': [
                     (
                      51, b'', b'', [], 61, b'inserted line', [], False),
                     (
                      100, b'', b'', [], 110, b'inserted line', [], False)]}]
        self.assertEqual(get_displayed_diff_line_ranges(chunks, 20, 69), (
         {b'display_range': (30, 60), 
            b'virtual_range': (20, 50), 
            b'chunk_range': (
                           chunks[0], chunks[0])},
         {b'display_range': (61, 79), 
            b'virtual_range': (51, 69), 
            b'chunk_range': (
                           chunks[1], chunks[1])}))


class DiffExpansionHeaderTests(TestCase):
    """Testing generation of diff expansion headers."""

    def test_find_header_with_filtered_equal(self):
        """Testing finding a header in a file that has filtered equals
        chunks
        """
        chunks = [
         {b'change': b'equal', 
            b'meta': {b'left_headers': [
                                      (1, 'foo')], 
                      b'right_headers': []}, 
            b'lines': [
                     {0: 1, 
                        1: 1, 
                        4: b''},
                     {0: 2, 
                        1: 2, 
                        4: 1}]},
         {b'change': b'equal', 
            b'meta': {b'left_headers': [], b'right_headers': [
                                       (2, 'bar')]}, 
            b'lines': [
                     {0: 3, 
                        1: b'', 
                        4: 2},
                     {0: 4, 
                        1: 3, 
                        4: 3}]}]
        left_header = {b'line': 1, 
           b'text': b'foo'}
        right_header = {b'line': 3, 
           b'text': b'bar'}
        self.assertEqual(_get_last_header_in_chunks_before_line(chunks, 2), {b'left': left_header, 
           b'right': None})
        self.assertEqual(_get_last_header_in_chunks_before_line(chunks, 4), {b'left': left_header, 
           b'right': right_header})
        return

    def test_find_header_with_header_oustside_chunk(self):
        """Testing finding a header in a file where the header in a chunk does
        not belong to the chunk it is in
        """
        chunks = [
         {b'change': b'equal', 
            b'meta': {b'left_headers': [
                                      (1, 'foo'),
                                      (100, 'bar')]}, 
            b'lines': [
                     {0: 1, 
                        1: 1, 
                        4: 1},
                     {0: 2, 
                        1: 2, 
                        4: 1}]}]
        self.assertEqual(_get_last_header_in_chunks_before_line(chunks, 2), {b'left': {b'line': 1, 
                     b'text': b'foo'}, 
           b'right': None})
        return

    @add_fixtures([b'test_users', b'test_scmtools'])
    def test_headers_use_correct_line_insert(self):
        """Testing header generation for chunks with insert chunks above"""
        line_number = 27
        diff = b"diff --git a/tests.py b/tests.py\nindex a4fc53e..f2414cc 100644\n--- a/tests.py\n+++ b/tests.py\n@@ -20,6 +20,9 @@ from reviewboard.site.urlresolvers import local_site_reverse\n from reviewboard.site.models import LocalSite\n from reviewboard.webapi.errors import INVALID_REPOSITORY\n\n+class Foo(object):\n+    def bar(self):\n+        pass\n\n class BaseWebAPITestCase(TestCase, EmailTestHelper);\n     fixtures = ['test_users', 'test_reviewrequests', 'test_scmtools',\n"
        repository = self.create_repository(tool_name=b'Git')
        review_request = self.create_review_request(repository=repository)
        diffset = self.create_diffset(review_request=review_request)
        filediff = self.create_filediff(diffset=diffset, source_file=b'tests.py', dest_file=b'tests.py', source_revision=b'a4fc53e08863f5341effb5204b77504c120166ae', diff=diff)
        context = {b'user': review_request.submitter}
        siteconfig_settings = {b'diffviewer_syntax_highlighting': False}
        with self.siteconfig_settings(siteconfig_settings, reload_settings=False):
            header = get_last_header_before_line(context=context, filediff=filediff, interfilediff=None, target_line=line_number)
            chunks = get_file_chunks_in_range(context=context, filediff=filediff, interfilediff=None, first_line=1, num_lines=get_last_line_number_in_diff(context=context, filediff=filediff, interfilediff=None))
        lines = []
        for chunk in chunks:
            lines.extend(chunk[b'lines'])

        self.assertTrue(header[b'right'][b'line'] < line_number)
        self.assertEqual(header[b'right'][b'text'], lines[(header[b'right'][b'line'] - 1)][5])
        return

    @add_fixtures([b'test_users', b'test_scmtools'])
    def test_header_correct_line_delete(self):
        """Testing header generation for chunks with delete chunks above"""
        line_number = 53
        diff = b"diff --git a/tests.py b/tests.py\nindex a4fc53e..ba7d34b 100644\n--- a/tests.py\n+++ b/tests.py\n@@ -47,9 +47,6 @@ class BaseWebAPITestCase(TestCase, EmailTestHelper);\n\n         yourself.base_url = 'http;//testserver'\n\n-    def tearDown(yourself);\n-        yourself.client.logout()\n-\n     def api_func_wrapper(yourself, api_func, path, query, expected_status,\n                          follow_redirects, expected_redirects);\n         response = api_func(path, query, follow=follow_redirects)\n"
        repository = self.create_repository(tool_name=b'Git')
        review_request = self.create_review_request(repository=repository)
        diffset = self.create_diffset(review_request=review_request)
        filediff = self.create_filediff(diffset=diffset, source_file=b'tests.py', dest_file=b'tests.py', source_revision=b'a4fc53e08863f5341effb5204b77504c120166ae', diff=diff)
        context = {b'user': review_request.submitter}
        siteconfig_settings = {b'diffviewer_syntax_highlighting': False}
        with self.siteconfig_settings(siteconfig_settings, reload_settings=False):
            header = get_last_header_before_line(context=context, filediff=filediff, interfilediff=None, target_line=line_number)
            chunks = get_file_chunks_in_range(context=context, filediff=filediff, interfilediff=None, first_line=1, num_lines=get_last_line_number_in_diff(context=context, filediff=filediff, interfilediff=None))
        lines = []
        for chunk in chunks:
            lines.extend(chunk[b'lines'])

        self.assertTrue(header[b'left'][b'line'] < line_number)
        self.assertEqual(header[b'left'][b'text'], lines[(header[b'left'][b'line'] - 1)][2])
        return


class PatchTests(TestCase):
    """Unit tests for patch."""

    def test_patch(self):
        """Testing patch"""
        old = b'int\nmain()\n{\n\tprintf("foo\\n");\n}\n'
        new = b'#include <stdio.h>\n\nint\nmain()\n{\n\tprintf("foo bar\\n");\n\treturn 0;\n}\n'
        diff = b'--- foo.c\t2007-01-24 02:11:31.000000000 -0800\n+++ foo.c\t2007-01-24 02:14:42.000000000 -0800\n@@ -1,5 +1,8 @@\n+#include <stdio.h>\n+\n int\n main()\n {\n-\tprintf("foo\\n");\n+\tprintf("foo bar\\n");\n+\treturn 0;\n }\n'
        patched = patch(diff, old, b'foo.c')
        self.assertEqual(patched, new)
        diff = b"--- README\t2007-01-24 02:10:28.000000000 -0800\n+++ README\t2007-01-24 02:11:01.000000000 -0800\n@@ -1,9 +1,10 @@\n Test data for a README file.\n \n There's a line here.\n-\n A line there.\n \n And here.\n"
        with self.assertRaises(Exception):
            patch(diff, old, b'foo.c')

    def test_empty_patch(self):
        """Testing patch with an empty diff"""
        old = b'This is a test'
        diff = b''
        patched = patch(diff, old, b'test.c')
        self.assertEqual(patched, old)

    def test_patch_crlf_file_crlf_diff(self):
        """Testing patch with a CRLF file and a CRLF diff"""
        old = b"Test data for a README file.\r\n\r\nThere's a line here.\r\n\r\nA line there.\r\n\r\nAnd here.\r\n"
        new = b"Test data for a README file.\n\nThere's a line here.\nA line there.\n\nAnd here.\n"
        diff = b"--- README\t2007-07-02 23:33:27.000000000 -0700\n+++ README\t2007-07-02 23:32:59.000000000 -0700\n@@ -1,7 +1,6 @@\n Test data for a README file.\r\n \r\n There's a line here.\r\n-\r\n A line there.\r\n \r\n And here.\r\n"
        patched = patch(diff, old, new)
        self.assertEqual(patched, new)

    def test_patch_cr_file_crlf_diff(self):
        """Testing patch with a CR file and a CRLF diff"""
        old = b"Test data for a README file.\n\nThere's a line here.\n\nA line there.\n\nAnd here.\n"
        new = b"Test data for a README file.\n\nThere's a line here.\nA line there.\n\nAnd here.\n"
        diff = b"--- README\t2007-07-02 23:33:27.000000000 -0700\n+++ README\t2007-07-02 23:32:59.000000000 -0700\n@@ -1,7 +1,6 @@\n Test data for a README file.\r\n \r\n There's a line here.\r\n-\r\n A line there.\r\n \r\n And here.\r\n"
        patched = patch(diff, old, new)
        self.assertEqual(patched, new)

    def test_patch_crlf_file_cr_diff(self):
        """Testing patch with a CRLF file and a CR diff"""
        old = b"Test data for a README file.\r\n\r\nThere's a line here.\r\n\r\nA line there.\r\n\r\nAnd here.\r\n"
        new = b"Test data for a README file.\n\nThere's a line here.\nA line there.\n\nAnd here.\n"
        diff = b"--- README\t2007-07-02 23:33:27.000000000 -0700\n+++ README\t2007-07-02 23:32:59.000000000 -0700\n@@ -1,7 +1,6 @@\n Test data for a README file.\n \n There's a line here.\n-\n A line there.\n \n And here.\n"
        patched = patch(diff, old, new)
        self.assertEqual(patched, new)

    def test_patch_file_with_fake_no_newline(self):
        r"""Testing patch with a file indicating no newline
        with a trailing \r
        """
        old = b"Test data for a README file.\n\nThere's a line here.\n\nA line there.\n\nAnd a new line here!\n\nWe must have several lines to reproduce this problem.\n\nSo that there's enough hidden context.\n\nAnd dividers so we can reproduce the bug.\n\nWhich will a --- line at the end of one file due to the lack of newline,\ncausing a parse error.\n\nAnd here.\nYes, this is a good README file. Like most README files, this doesn't tell youanything you really didn't already know.\r"
        new = b"Test data for a README file.\n\nThere's a line here.\nHere's a change!\n\nA line there.\n\nAnd a new line here!\n\nWe must have several lines to reproduce this problem.\n\nSo that there's enough hidden context.\n\nAnd dividers so we can reproduce the bug.\n\nWhich will a --- line at the end of one file due to the lack of newline,\ncausing a parse error.\n\nAnd here.\nYes, this is a good README file. Like most README files, this doesn't tell youanything you really didn't already know.\n"
        diff = b"--- README\t2008-02-25 03:40:42.000000000 -0800\n+++ README\t2008-02-25 03:40:55.000000000 -0800\n@@ -1,6 +1,7 @@\n Test data for a README file.\n \n There's a line here.\n+Here's a change!\n \n A line there.\n \n@@ -16,4 +17,4 @@\n causing a parse error.\n \n And here.\n-Yes, this is a good README file. Like most README files, this doesn't tell youanything you really didn't already know.\n\\ No newline at end of file\n+Yes, this is a good README file. Like most README files, this doesn't tell youanything you really didn't already know.\n"
        patched = patch(diff, old, b'README')
        self.assertEqual(patched, new)


class GetOriginalFileTests(SpyAgency, TestCase):
    """Unit tests for get_original_file."""
    fixtures = [
     b'test_scmtools']

    def test_empty_parent_diff_old_patch(self):
        """Testing get_original_file with an empty parent diff with a patch
        tool that does not accept empty diffs
        """
        parent_diff = b'diff --git a/empty b/empty\nnew file mode 100644\nindex 0000000..e69de29\n'
        diff = b'diff --git a/empty b/empty\nindex e69de29..0e4b0c7 100644\n--- a/empty\n+++ a/empty\n@@ -0,0 +1 @@\n+abc123\n'
        repository = self.create_repository(tool_name=b'Git')
        diffset = self.create_diffset(repository=repository)
        filediff = FileDiff.objects.create(diffset=diffset, source_file=b'empty', source_revision=PRE_CREATION, dest_file=b'empty', dest_detail=b'0e4b0c7')
        filediff.parent_diff = parent_diff
        filediff.diff = diff
        filediff.save()
        request_factory = RequestFactory()

        def _patch(diff, orig_file, filename, request=None):
            self.assertEqual(diff, parent_diff)
            raise PatchError(filename=filename, error_output=_PATCH_GARBAGE_INPUT, orig_file=orig_file, new_file=b'tmp123-new', diff=b'', rejects=None)
            return

        self.spy_on(patch, call_fake=_patch)
        with self.assertNumQueries(2):
            orig = get_original_file(filediff=filediff, request=request_factory.get(b'/'), encoding_list=[
             b'ascii'])
        self.assertEqual(orig, b'')
        filediff = FileDiff.objects.filter(pk=filediff.pk).select_related(b'parent_diff_hash').first()
        with self.assertNumQueries(0):
            orig = get_original_file(filediff=filediff, request=request_factory.get(b'/'), encoding_list=[
             b'ascii'])
        return

    def test_empty_parent_diff_new_patch(self):
        """Testing get_original_file with an empty parent diff with a patch
        tool that does accept empty diffs
        """
        parent_diff = b'diff --git a/empty b/empty\nnew file mode 100644\nindex 0000000..e69de29\n'
        diff = b'diff --git a/empty b/empty\nindex e69de29..0e4b0c7 100644\n--- a/empty\n+++ a/empty\n@@ -0,0 +1 @@\n+abc123\n'
        repository = self.create_repository(tool_name=b'Git')
        diffset = self.create_diffset(repository=repository)
        filediff = FileDiff.objects.create(diffset=diffset, source_file=b'empty', source_revision=PRE_CREATION, dest_file=b'empty', dest_detail=b'0e4b0c7')
        filediff.parent_diff = parent_diff
        filediff.diff = diff
        filediff.save()
        request_factory = RequestFactory()

        def _patch(diff, orig_file, filename, request=None):
            self.assertEqual(diff, parent_diff)
            return orig_file

        self.spy_on(patch, call_fake=_patch)
        with self.assertNumQueries(0):
            orig = get_original_file(filediff=filediff, request=request_factory.get(b'/'), encoding_list=[
             b'ascii'])
        self.assertEqual(orig, b'')
        filediff = FileDiff.objects.select_related(b'parent_diff_hash').get(pk=filediff.pk)
        with self.assertNumQueries(0):
            orig = get_original_file(filediff=filediff, request=request_factory.get(b'/'), encoding_list=[
             b'ascii'])
        return