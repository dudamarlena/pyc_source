# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/checkpoint/tests/repository.py
# Compiled at: 2009-01-08 17:03:56
__doc__ = 'Unit-test the Checkpoint Repository'
from __future__ import with_statement
import os, shutil, tempfile, unittest
from checkpoint.filestore import FILE
from checkpoint.repository import Repository, Mirror, ADDED, DELETED, MODIFIED
from checkpoint.error import CheckpointError
from checkpoint.util import filter_all_patterns, matches_any_pattern
from checkpoint.tests.filestore import TempFileTestCase
__all__ = [
 'RepositoryTest', 'MirrorTest']

class RepositoryTest(TempFileTestCase):

    def setUp(self):
        TempFileTestCase.setUp(self)
        self.create_temp_files(self.test_files)

    def testInitializeRepository(self):
        """initialize should work"""
        self.repository = Repository(self.temp_dir)
        self.repository.initialize()
        self.assertTrue(os.path.isdir(self.repository.repository_path))
        self.assertTrue(Repository.contains_repository(self.temp_dir))
        self.assertTrue(self.repository.filestore.is_initialized())
        self.assertTrue(self.repository.db.is_initialized())
        repository_format_file = os.path.join(self.repository.repository_path, 'repository_format')
        self.assertTrue(os.path.exists(repository_format_file))
        self.assertRaises(CheckpointError, self.repository.initialize)

    def testDeleteRepository(self):
        """delete should work"""
        self.testInitializeRepository()
        self.repository.delete_repository()
        self.assertFalse(os.path.isdir(self.repository.repository_path))
        self.assertRaises(CheckpointError, self.repository.delete_repository)

    def testCommit(self):
        """iter_changes should detect no new changes after commit"""
        self.testInitializeRepository()
        self.repository.commit()
        self.assertTrue(list(self.repository.iter_changes()) == [])

    def testAddFiles(self):
        """iter_changes should detect new files"""
        self.testCommit()
        self.new_file = 'some-new-file.txt'
        with open(self.format_path(self.new_file), 'w') as (f):
            f.write('hi there')
        changes = list(self.repository.iter_changes())
        self.assertTrue(len(changes) == 1)
        (path, path_hash, fingerprint, file_type, status) = changes[0]
        self.assertTrue(path == self.new_file)
        self.assertTrue(file_type == FILE)
        self.assertTrue(status == ADDED)
        self.repository.commit()
        self.assertTrue(list(self.repository.iter_changes()) == [])

    def testDeleteFiles(self):
        """iter_changes should detect deleted files"""
        self.testAddFiles()
        os.remove(self.format_path(self.new_file))
        changes = list(self.repository.iter_changes())
        self.assertTrue(len(changes) == 1)
        (path, path_hash, fingerprint, file_type, status) = changes[0]
        self.assertTrue(path == self.new_file)
        self.assertTrue(file_type == FILE)
        self.assertTrue(status == DELETED)
        self.repository.commit()
        self.assertTrue(list(self.repository.iter_changes()) == [])

    def testModifiedFiles(self):
        """iter_changes should detect modified files"""
        self.testAddFiles()
        import time
        time.sleep(1)
        with open(self.format_path(self.new_file), 'w') as (f):
            f.write('this is some amazing new content!')
        changes = list(self.repository.iter_changes())
        self.assertTrue(len(changes) == 1)
        (path, path_hash, fingerprint, file_type, status) = changes[0]
        self.assertTrue(path == self.new_file)
        self.assertTrue(file_type == FILE)
        self.assertTrue(status == MODIFIED)
        self.repository.commit()
        self.assertTrue(list(self.repository.iter_changes()) == [])

    def testRevertUncommittedChanges(self):
        """revert should properly undo recent changes"""
        self.testAddFiles()
        self.assertTrue(list(self.repository.iter_changes()) == [])
        other_file = self.format_path('otherfile.txt')
        with open(other_file, 'w') as (f):
            f.write('some other data')
        self.assertTrue(os.path.exists(other_file))
        self.assertTrue(len(list(self.repository.iter_changes())) == 1)
        self.repository.revert()
        self.assertFalse(os.path.exists(other_file))
        self.assertTrue(list(self.repository.iter_changes()) == [])

    def testRevertLots(self):
        """revert should be able to undo all the way back to changset 1"""
        self.testModifiedFiles()
        self.repository.revert(changeset=1)
        original_files = [ x.split('->')[0] for x in self.test_files ]
        for path in original_files:
            self.assertTrue(os.path.exists(self.format_path(path)))

        ignored_patterns = self.repository.get_ignored_patterns()
        for (root, dirs, files) in os.walk(self.format_path('')):
            files = filter_all_patterns(files, ignored_patterns)
            for d in dirs:
                if matches_any_pattern(d, ignored_patterns):
                    dirs.remove(d)

            dirs = [ '%s/' % d for d in dirs ]
            for x in dirs + files:
                abspath = os.path.join(root, x)
                relpath = self.repository.get_relpath(abspath)
                self.assertTrue(relpath in original_files)

    def testPortability(self):
        """Checkpoint directories should continue working when moved."""
        self.testCommit()
        old_temp_dir = self.temp_dir
        new_temp_dir = os.path.join(tempfile.gettempdir(), 'moved')
        os.chdir(tempfile.gettempdir())
        os.rename(old_temp_dir, new_temp_dir)
        self.repository = Repository(new_temp_dir)
        changes = list(self.repository.iter_changes())
        self.assertTrue(len(changes) == 0)
        os.rename(new_temp_dir, old_temp_dir)


class MirrorTest(TempFileTestCase):
    pass


if __name__ == '__main__':
    unittest.main()