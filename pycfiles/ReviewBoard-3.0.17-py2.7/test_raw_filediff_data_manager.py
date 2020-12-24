# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/diffviewer/tests/test_raw_filediff_data_manager.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
import bz2
from reviewboard.diffviewer.models import RawFileDiffData
from reviewboard.testing import TestCase

class RawFileDiffDataManagerTests(TestCase):
    """Unit tests for RawFileDiffDataManager."""
    small_diff = b'diff --git a/README b/README\nindex d6613f5..5b50866 100644\n--- README\n+++ README\n@ -1,1 +1,1 @@\n-blah blah\n+blah!\n'
    large_diff = b'diff --git a/README b/README\nindex d6613f5..5b50866 100644\n--- README\n+++ README\n@ -1,1 +1,10 @@\n-blah blah\n+blah!\n+blah!\n+blah!\n+blah!\n+blah!\n+blah!\n+blah!\n+blah!\n+blah!\n+blah!\n'

    def test_process_diff_data_small_diff_uncompressed(self):
        """Testing RawFileDiffDataManager.process_diff_data with small diff
        results in uncompressed storage
        """
        data, compression = RawFileDiffData.objects.process_diff_data(self.small_diff)
        self.assertEqual(data, self.small_diff)
        self.assertIsNone(compression)

    def test_process_diff_data_large_diff_compressed(self):
        """Testing RawFileDiffDataManager.process_diff_data with large diff
        results in bzip2-compressed storage
        """
        data, compression = RawFileDiffData.objects.process_diff_data(self.large_diff)
        self.assertEqual(data, bz2.compress(self.large_diff, 9))
        self.assertEqual(compression, RawFileDiffData.COMPRESSION_BZIP2)