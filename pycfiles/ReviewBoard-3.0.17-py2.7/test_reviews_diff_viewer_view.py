# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/reviews/tests/test_reviews_diff_viewer_view.py
# Compiled at: 2020-02-11 04:03:56
"""Unit tests for reviewboard.reviews.views.ReviewsDiffViewerView."""
from __future__ import unicode_literals
from reviewboard.site.urlresolvers import local_site_reverse
from reviewboard.testing import TestCase

class ReviewsDiffViewerViewTests(TestCase):
    """Unit tests for reviewboard.reviews.views.ReviewsDiffViewerView."""
    fixtures = [
     b'test_users', b'test_scmtools']

    def test_interdiff(self):
        """Testing ReviewsDiffViewerView with interdiffs"""
        review_request = self.create_review_request(create_repository=True, publish=True)
        diffset = self.create_diffset(review_request, revision=1)
        self.create_filediff(diffset, source_file=b'/diffutils.py', dest_file=b'/diffutils.py', source_revision=b'6bba278', dest_detail=b'465d217', diff=b'diff --git a/diffutils.py b/diffutils.py\nindex 6bba278..465d217 100644\n--- a/diffutils.py\n+++ b/diffutils.py\n@@ -1,3 +1,4 @@\n+# diffutils.py\n import fnmatch\n import os\n import re\n')
        self.create_filediff(diffset, source_file=b'/readme', dest_file=b'/readme', source_revision=b'd6613f5', dest_detail=b'5b50866', diff=b'diff --git a/readme b/readme\nindex d6613f5..5b50866 100644\n--- a/readme\n+++ b/readme\n@@ -1 +1,3 @@\n Hello there\n+\n+Oh hi!\n')
        self.create_filediff(diffset, source_file=b'/newfile', dest_file=b'/newfile', source_revision=b'PRE-CREATION', dest_detail=b'', diff=b'diff --git a/new_file b/new_file\nnew file mode 100644\nindex 0000000..ac30bd3\n--- /dev/null\n+++ b/new_file\n@@ -0,0 +1 @@\n+This is a new file!\n')
        diffset = self.create_diffset(review_request, revision=2)
        self.create_filediff(diffset, source_file=b'/diffutils.py', dest_file=b'/diffutils.py', source_revision=b'6bba278', dest_detail=b'465d217', diff=b'diff --git a/diffutils.py b/diffutils.py\nindex 6bba278..465d217 100644\n--- a/diffutils.py\n+++ b/diffutils.py\n@@ -1,3 +1,4 @@\n+# diffutils.py\n import fnmatch\n import os\n import re\n')
        self.create_filediff(diffset, source_file=b'/readme', dest_file=b'/readme', source_revision=b'd6613f5', dest_detail=b'5b50867', diff=b'diff --git a/readme b/readme\nindex d6613f5..5b50867 100644\n--- a/readme\n+++ b/readme\n@@ -1 +1,3 @@\n Hello there\n+----------\n+Oh hi!\n')
        self.create_filediff(diffset, source_file=b'/newfile', dest_file=b'/newfile', source_revision=b'PRE-CREATION', dest_detail=b'', diff=b'diff --git a/new_file b/new_file\nnew file mode 100644\nindex 0000000..ac30bd4\n--- /dev/null\n+++ b/new_file\n@@ -0,0 +1 @@\n+This is a diffent version of this new file!\n')
        response = self.client.get(b'/r/1/diff/1-2/')
        if response.status_code != 200:
            print b'Error: %s' % response.context[b'error']
            print response.context[b'trace']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[b'diff_context'][b'num_diffs'], 2)
        files = response.context[b'files']
        self.assertTrue(files)
        self.assertEqual(len(files), 2)
        self.assertEqual(files[0][b'depot_filename'], b'/newfile')
        self.assertIn(b'interfilediff', files[0])
        self.assertEqual(files[1][b'depot_filename'], b'/readme')
        self.assertIn(b'interfilediff', files[1])

    def test_interdiff_new_file(self):
        """Testing ReviewsDiffViewrView with interdiffs containing new files"""
        review_request = self.create_review_request(create_repository=True, publish=True)
        diffset = self.create_diffset(review_request, revision=1)
        self.create_filediff(diffset, source_file=b'/diffutils.py', dest_file=b'/diffutils.py', source_revision=b'6bba278', dest_detail=b'465d217', diff=b'diff --git a/diffutils.py b/diffutils.py\nindex 6bba278..465d217 100644\n--- a/diffutils.py\n+++ b/diffutils.py\n@@ -1,3 +1,4 @@\n+# diffutils.py\n import fnmatch\n import os\n import re\n')
        diffset = self.create_diffset(review_request, revision=2)
        self.create_filediff(diffset, source_file=b'/diffutils.py', dest_file=b'/diffutils.py', source_revision=b'6bba278', dest_detail=b'465d217', diff=b'diff --git a/diffutils.py b/diffutils.py\nindex 6bba278..465d217 100644\n--- a/diffutils.py\n+++ b/diffutils.py\n@@ -1,3 +1,4 @@\n+# diffutils.py\n import fnmatch\n import os\n import re\n')
        self.create_filediff(diffset, source_file=b'/newfile', dest_file=b'/newfile', source_revision=b'PRE-CREATION', dest_detail=b'', diff=b'diff --git a/new_file b/new_file\nnew file mode 100644\nindex 0000000..ac30bd4\n--- /dev/null\n+++ b/new_file\n@@ -0,0 +1 @@\n+This is a diffent version of this new file!\n')
        response = self.client.get(b'/r/1/diff/1-2/')
        if response.status_code != 200:
            print b'Error: %s' % response.context[b'error']
            print response.context[b'trace']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context[b'diff_context'][b'num_diffs'], 2)
        files = response.context[b'files']
        self.assertTrue(files)
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0][b'depot_filename'], b'/newfile')
        self.assertIn(b'interfilediff', files[0])

    def test_with_filenames_option(self):
        """Testing ReviewsDiffViewerView with ?filenames=..."""
        review_request = self.create_review_request(create_repository=True, publish=True)
        diffset = self.create_diffset(review_request)
        filediff1 = self.create_filediff(diffset, source_file=b'src/main/test.c', dest_file=b'src/main/test.cpp')
        filediff2 = self.create_filediff(diffset, source_file=b'docs/README.txt', dest_file=b'docs/README2.txt')
        filediff3 = self.create_filediff(diffset, source_file=b'test.txt', dest_file=b'test.rst')
        filediff4 = self.create_filediff(diffset, source_file=b'/lib/lib.h', dest_file=b'/lib/lib.h')
        self.create_filediff(diffset, source_file=b'unmatched', dest_file=b'unmatched')
        response = self.client.get(local_site_reverse(b'view-diff-revision', kwargs={b'review_request_id': review_request.display_id, 
           b'revision': diffset.revision}), {b'filenames': b'*/test.cpp,*.txt,/lib/*'})
        self.assertEqual(response.status_code, 200)
        files = response.context[b'files']
        self.assertEqual({file_info[b'filediff'] for file_info in files}, {
         filediff1, filediff2, filediff3, filediff4})

    def test_with_filenames_option_normalized(self):
        """Testing ReviewsDiffViewerView with ?filenames=... values normalized
        """
        review_request = self.create_review_request(create_repository=True, publish=True)
        diffset = self.create_diffset(review_request)
        filediff1 = self.create_filediff(diffset, source_file=b'src/main/test.c', dest_file=b'src/main/test.cpp')
        filediff2 = self.create_filediff(diffset, source_file=b'docs/README.txt', dest_file=b'docs/README2.txt')
        filediff3 = self.create_filediff(diffset, source_file=b'test.txt', dest_file=b'test.rst')
        filediff4 = self.create_filediff(diffset, source_file=b'/lib/lib.h', dest_file=b'/lib/lib.h')
        self.create_filediff(diffset, source_file=b'unmatched', dest_file=b'unmatched')
        response = self.client.get(local_site_reverse(b'view-diff-revision', kwargs={b'review_request_id': review_request.display_id, 
           b'revision': diffset.revision}), {b'filenames': b' ,  , */test.cpp,,,*.txt,/lib/*  '})
        self.assertEqual(response.status_code, 200)
        files = response.context[b'files']
        self.assertEqual({file_info[b'filediff'] for file_info in files}, {
         filediff1, filediff2, filediff3, filediff4})