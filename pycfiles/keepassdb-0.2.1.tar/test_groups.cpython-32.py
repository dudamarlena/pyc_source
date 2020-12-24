# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hans/workspace/keepassdb/tests/test_groups.py
# Compiled at: 2012-12-30 21:26:20
"""
Unit tests for group-related operations.
"""
from __future__ import print_function
import os.path
from keepassdb import Database
from tests import TestBase, RESOURCES_DIR

class GroupTest(TestBase):

    def test_move(self):
        """ Test moving group to another level. """
        db = Database(os.path.join(RESOURCES_DIR, 'example.kdb'), password='test')
        group = self.get_group_by_name(db, 'B1')
        new_parent = self.get_group_by_name(db, 'A1')
        print(new_parent)
        group.move(new_parent)
        print('After move: ' + repr(group.parent))
        self.assertEquals(new_parent, group.parent)
        a1 = db.root.children[0].children[0]
        self.assertEquals(['A2', 'B1'], [g.title for g in a1.children])

    def test_move_index(self):
        """ Test moving group to another location in same parent. """
        db = Database(os.path.join(RESOURCES_DIR, 'example.kdb'), password='test')
        i_g = db.root.children[0]
        self.assertEquals(['A1', 'B1', 'C1'], [g.title for g in i_g.children])
        group = self.get_group_by_name(db, 'C1')
        orig_parent = group.parent
        group.move(orig_parent, 0)
        self.assertIs(orig_parent, group.parent)
        i_g = db.root.children[0]
        self.assertEquals(['C1', 'A1', 'B1'], [g.title for g in i_g.children])