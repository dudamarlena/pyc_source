# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/eric/github/local/gitberg/gitenberg/tests/test_local_repo.py
# Compiled at: 2020-01-02 17:42:20
import os, shutil, unittest, git
from gitenberg.local_repo import LocalRepo

class TestLocalRepo(unittest.TestCase):
    relative_test_repo_path = './gitenberg/tests/test_data/test_repo'

    def setUp(self):
        git.Repo.init(self.relative_test_repo_path)
        self.local_repo = LocalRepo(self.relative_test_repo_path)

    def tearDown(self):
        shutil.rmtree(self.relative_test_repo_path)

    def _touch_file(self, name):
        path = os.path.join(self.relative_test_repo_path, name)
        with open(path, 'a'):
            os.utime(path, None)
        return

    def test_add_file(self):
        self._touch_file('foof')
        self.local_repo.add_file('foof')
        self.assertEqual(set(self.local_repo.git.index.entries.keys()), {
         ('foof', 0)})

    def test_add_all_files(self):
        [ self._touch_file(f) for f in ['foof', 'offo.txt', 'fofo.md'] ]
        self.local_repo.add_all_files()
        self.assertEqual(set(self.local_repo.git.index.entries.keys()), {
         ('fofo.md', 0), ('offo.txt', 0), ('foof', 0)})

    def test_add_all_files_filters_ignore_list(self):
        [ self._touch_file(f) for f in ['offo.txt', 'fofo.ogg', 'zoom'] ]
        self.local_repo.add_all_files()
        self.assertEqual(list(self.local_repo.git.index.entries.keys()), [
         ('offo.txt', 0), ('zoom', 0)])

    def test_commit(self):
        file_name = 'foom.txt'
        message = 'this is a commit messaage'
        self._touch_file(file_name)
        self.local_repo.add_file(file_name)
        self.local_repo.commit(message)
        latest_commit = self.local_repo.git.heads.master.commit
        self.assertEqual(latest_commit.message, message)

    def test_file_checks(self):
        self.assertFalse(self.local_repo.metadata_file)