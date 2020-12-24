# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/diffviewer/tests/test_diffset.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import unicode_literals
from reviewboard.diffviewer.models import DiffSet, DiffSetHistory
from reviewboard.testing import TestCase

class DiffSetTests(TestCase):
    """Unit tests for reviewboard.diffviewer.models.DiffSet."""
    fixtures = [
     b'test_scmtools']

    def test_update_revision_from_history_with_diffsets(self):
        """Testing DiffSet.update_revision_from_history with existing diffsets
        """
        repository = self.create_repository(tool_name=b'Test')
        diffset_history = DiffSetHistory.objects.create()
        diffset_history.diffsets.add(self.create_diffset(repository=repository))
        diffset = DiffSet()
        diffset.update_revision_from_history(diffset_history)
        self.assertEqual(diffset.revision, 2)

    def test_update_revision_from_history_without_diffsets(self):
        """Testing DiffSet.update_revision_from_history without existing
        diffsets
        """
        diffset_history = DiffSetHistory.objects.create()
        diffset = DiffSet()
        diffset.update_revision_from_history(diffset_history)
        self.assertEqual(diffset.revision, 1)

    def test_update_revision_from_history_with_revision_already_set(self):
        """Testing DiffSet.update_revision_from_history with revision
        already set
        """
        diffset_history = DiffSetHistory.objects.create()
        diffset = DiffSet(revision=1)
        with self.assertRaises(ValueError):
            diffset.update_revision_from_history(diffset_history)