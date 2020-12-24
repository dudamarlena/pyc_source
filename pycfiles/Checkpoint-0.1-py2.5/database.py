# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/checkpoint/tests/database.py
# Compiled at: 2009-01-06 11:27:52
"""Unit-test the Checkpoint Database system"""
import os, shutil, errno, tempfile, unittest
from checkpoint.error import *
from checkpoint.database import Database
from checkpoint.filestore import FILE, LINK, DIRECTORY
from checkpoint.repository import ADDED, DELETED
__all__ = [
 'DatabaseTest']

class DatabaseTest(unittest.TestCase):

    def setUp(self):
        """Prepare test environment (basic setup shared between all tests)."""
        self.temp_dir = os.path.join(tempfile.gettempdir(), 'databasetests')
        try:
            shutil.rmtree(self.temp_dir)
        except OSError, e:
            if e.errno != errno.ENOENT:
                raise

        os.mkdir(self.temp_dir)
        os.chdir(self.temp_dir)
        self.repository = os.path.join(self.temp_dir, '.cpt')
        os.mkdir(self.repository)
        self.db = Database(self.repository)

    def tearDown(self):
        """Remove resources used by test environment."""
        os.chdir(self.temp_dir)
        os.chdir(os.pardir)
        shutil.rmtree(self.temp_dir)

    def testRepositoryNotInitialized(self):
        """Uninitialized Databases should raise an error on access."""
        self.assertRaises(UninitializedRepositoryError, self.db.select, 'modifications')

    def testInsert(self):
        """INSERTs should work."""
        self.db.initialize()
        self.assertFalse(self.db.select('changeset').fetchone())
        new_changeset = self.db.insert('changeset', dict(id=None)).lastrowid
        self.assertTrue(self.db.select('changeset').fetchone())
        self.assertTrue(new_changeset is not None)
        return new_changeset

    def testGetCurrentChangeset(self):
        """get_current_changeset should return the latest changeset id."""
        new_changeset = self.testInsert()
        self.assertTrue(self.db.get_current_changeset() == new_changeset)

    def testRecordPaths(self):
        """record_added should work."""
        self.path_infos = [
         (
          '/path/a.txt', 'test-hash-1', 'test-hash-2', FILE, ADDED),
         (
          '/path/b.txt', 'test-hash-3', 'test-hash-4', LINK, ADDED),
         (
          '/path/more', 'test-hash-5', 'test-hash-6', DIRECTORY, ADDED)]
        new_changeset = self.testInsert()
        for x in self.path_infos:
            self.db.record_added(new_changeset, *x)

        for x in self.path_infos:
            results = self.db.select('modification', [
             'hash', 'fingerprint', 'type', 'status'], dict(path=x[0])).fetchone()
            self.assertTrue(results == x[1:])

        for x in self.path_infos:
            self.assertTrue(self.db.get_active_hash(x[0]) == x[1])
            self.assertTrue(self.db.get_active_fingerprint(x[0]) == x[2])
            self.assertTrue(self.db.get_active_file_type(x[0]) == x[3])

    def testPathDeletions(self):
        """record_deleted should work."""
        self.testRecordPaths()
        new_changeset = self.db.insert('changeset', dict(id=None)).lastrowid
        for x in self.path_infos:
            data = list(x[:-1]) + [DELETED]
            self.db.record_deleted(new_changeset, *data)

        for x in self.path_infos:
            data = list(x[:-1]) + [DELETED]
            results = self.db.select('modification', [
             'hash', 'fingerprint', 'type', 'status'], dict(path=data[0], status=DELETED)).fetchone()
            self.assertTrue(list(results) == list(data[1:]))

        return

    def testGetPreviousVersion(self):
        """get_previous_version should work"""
        self.testPathDeletions()
        changeset = self.db.get_current_changeset()
        for x in self.path_infos:
            path = x[0]
            results = self.db.get_previous_version(path, changeset)
            self.assertTrue(list(results) == list(x[1:]))


if __name__ == '__main__':
    unittest.main()