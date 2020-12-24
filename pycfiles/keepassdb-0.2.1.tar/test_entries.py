# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hans/workspace/keepassdb/keepassdb/tests/test_entries.py
# Compiled at: 2012-12-30 21:58:54
"""
Unit tests for group-related operations.
"""
from __future__ import print_function, unicode_literals
import os.path
from keepassdb import Database
from keepassdb.tests import TestBase, RESOURCES_DIR

class EntryTest(TestBase):

    def test_move(self):
        """ Test moving an entry to a new group. """
        db = Database(os.path.join(RESOURCES_DIR, b'example.kdb'), password=b'test')
        new_parent = self.get_group_by_name(db, b'A1')
        entry = self.get_entry_by_name(db, b'B1Entry1')
        orig_parent = entry.group
        self.assertEquals(b'B1', orig_parent.title)
        self.assertEquals([b'AEntry2', b'AEntry1', b'AEntry3'], [ e.title for e in new_parent.entries ])
        entry.move(new_parent)
        self.assertIs(new_parent, entry.group)
        self.assertEquals([b'AEntry2', b'AEntry1', b'AEntry3', b'B1Entry1'], [ e.title for e in new_parent.entries ])

    def test_move_index(self):
        """ Test moving an entry to a new group with index. """
        db = Database(os.path.join(RESOURCES_DIR, b'example.kdb'), password=b'test')
        new_parent = self.get_group_by_name(db, b'A1')
        entry = self.get_entry_by_name(db, b'B1Entry1')
        orig_parent = entry.group
        self.assertEquals(b'B1', orig_parent.title)
        self.assertEquals([b'AEntry2', b'AEntry1', b'AEntry3'], [ e.title for e in new_parent.entries ])
        entry.move(new_parent, 0)
        self.assertIs(new_parent, entry.group)
        self.assertEquals([b'B1Entry1', b'AEntry2', b'AEntry1', b'AEntry3'], [ e.title for e in new_parent.entries ])

    def test_move_within_group(self):
        """ Test moving an entry within the same group. """
        db = Database(os.path.join(RESOURCES_DIR, b'example.kdb'), password=b'test')
        new_parent = self.get_group_by_name(db, b'A1')
        entry = self.get_entry_by_name(db, b'AEntry2')
        self.assertEquals([b'AEntry2', b'AEntry1', b'AEntry3'], [ e.title for e in new_parent.entries ])
        entry.move(entry.group, 1)
        self.assertEquals([b'AEntry1', b'AEntry2', b'AEntry3'], [ e.title for e in new_parent.entries ])