# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dzhiltsov/Development/vcslib/managevcs/tests/test_repository.py
# Compiled at: 2015-06-08 06:25:01
from __future__ import with_statement
import datetime
from managevcs.tests.base import BackendTestMixin
from managevcs.tests.conf import SCM_TESTS
from managevcs.tests.conf import TEST_USER_CONFIG_FILE
from managevcs.nodes import FileNode
from managevcs.utils.compat import unittest
from managevcs.exceptions import ChangesetDoesNotExistError

class RepositoryBaseTest(BackendTestMixin):
    recreate_repo_per_test = False

    @classmethod
    def _get_commits(cls):
        return super(RepositoryBaseTest, cls)._get_commits()[:1]

    def test_get_config_value(self):
        self.assertEqual(self.repo.get_config_value('universal', 'foo', TEST_USER_CONFIG_FILE), 'bar')

    def test_get_config_value_defaults_to_None(self):
        self.assertEqual(self.repo.get_config_value('universal', 'nonexist', TEST_USER_CONFIG_FILE), None)
        return

    def test_get_user_name(self):
        self.assertEqual(self.repo.get_user_name(TEST_USER_CONFIG_FILE), 'Foo Bar')

    def test_get_user_email(self):
        self.assertEqual(self.repo.get_user_email(TEST_USER_CONFIG_FILE), 'foo.bar@example.com')

    def test_repo_equality(self):
        self.assertTrue(self.repo == self.repo)

    def test_repo_equality_broken_object(self):
        import copy
        _repo = copy.copy(self.repo)
        delattr(_repo, 'path')
        self.assertTrue(self.repo != _repo)

    def test_repo_equality_other_object(self):

        class dummy(object):
            path = self.repo.path

        self.assertTrue(self.repo != dummy())


class RepositoryGetDiffTest(BackendTestMixin):

    @classmethod
    def _get_commits(cls):
        commits = [
         {'message': 'Initial commit', 
            'author': 'Joe Doe <joe.doe@example.com>', 
            'date': datetime.datetime(2010, 1, 1, 20), 
            'added': [
                    FileNode('foobar', content='foobar'),
                    FileNode('foobar2', content='foobar2')]},
         {'message': 'Changed foobar, added foobar3', 
            'author': 'Jane Doe <jane.doe@example.com>', 
            'date': datetime.datetime(2010, 1, 1, 21), 
            'added': [
                    FileNode('foobar3', content='foobar3')], 
            'changed': [
                      FileNode('foobar', 'FOOBAR')]},
         {'message': 'Removed foobar, changed foobar3', 
            'author': 'Jane Doe <jane.doe@example.com>', 
            'date': datetime.datetime(2010, 1, 1, 22), 
            'changed': [
                      FileNode('foobar3', content='FOOBAR\nFOOBAR\nFOOBAR\n')], 
            'removed': [
                      FileNode('foobar')]}]
        return commits

    def test_raise_for_wrong(self):
        with self.assertRaises(ChangesetDoesNotExistError):
            self.repo.get_diff('a' * 40, 'b' * 40)


class GitRepositoryGetDiffTest(RepositoryGetDiffTest, unittest.TestCase):
    backend_alias = 'git'

    def test_initial_commit_diff(self):
        initial_rev = self.repo.revisions[0]
        self.assertEqual(self.repo.get_diff(self.repo.EMPTY_CHANGESET, initial_rev), 'diff --git a/foobar b/foobar\nnew file mode 100644\nindex 0000000000000000000000000000000000000000..f6ea0495187600e7b2288c8ac19c5886383a4632\n--- /dev/null\n+++ b/foobar\n@@ -0,0 +1 @@\n+foobar\n\\ No newline at end of file\ndiff --git a/foobar2 b/foobar2\nnew file mode 100644\nindex 0000000000000000000000000000000000000000..e8c9d6b98e3dce993a464935e1a53f50b56a3783\n--- /dev/null\n+++ b/foobar2\n@@ -0,0 +1 @@\n+foobar2\n\\ No newline at end of file\n')

    def test_second_changeset_diff(self):
        revs = self.repo.revisions
        self.assertEqual(self.repo.get_diff(revs[0], revs[1]), 'diff --git a/foobar b/foobar\nindex f6ea0495187600e7b2288c8ac19c5886383a4632..389865bb681b358c9b102d79abd8d5f941e96551 100644\n--- a/foobar\n+++ b/foobar\n@@ -1 +1 @@\n-foobar\n\\ No newline at end of file\n+FOOBAR\n\\ No newline at end of file\ndiff --git a/foobar3 b/foobar3\nnew file mode 100644\nindex 0000000000000000000000000000000000000000..c11c37d41d33fb47741cff93fa5f9d798c1535b0\n--- /dev/null\n+++ b/foobar3\n@@ -0,0 +1 @@\n+foobar3\n\\ No newline at end of file\n')

    def test_third_changeset_diff(self):
        revs = self.repo.revisions
        self.assertEqual(self.repo.get_diff(revs[1], revs[2]), 'diff --git a/foobar b/foobar\ndeleted file mode 100644\nindex 389865bb681b358c9b102d79abd8d5f941e96551..0000000000000000000000000000000000000000\n--- a/foobar\n+++ /dev/null\n@@ -1 +0,0 @@\n-FOOBAR\n\\ No newline at end of file\ndiff --git a/foobar3 b/foobar3\nindex c11c37d41d33fb47741cff93fa5f9d798c1535b0..f9324477362684ff692aaf5b9a81e01b9e9a671c 100644\n--- a/foobar3\n+++ b/foobar3\n@@ -1 +1,3 @@\n-foobar3\n\\ No newline at end of file\n+FOOBAR\n+FOOBAR\n+FOOBAR\n')


for alias in SCM_TESTS:
    attrs = {'backend_alias': alias}
    cls_name = alias.capitalize() + RepositoryBaseTest.__name__
    bases = (RepositoryBaseTest, unittest.TestCase)
    globals()[cls_name] = type(cls_name, bases, attrs)

if __name__ == '__main__':
    unittest.main()