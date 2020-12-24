# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dzhiltsov/Development/vcslib/managevcs/tests/test_diffs.py
# Compiled at: 2015-06-08 06:25:02
import datetime
from managevcs.tests.base import BackendTestMixin
from managevcs.tests.conf import SCM_TESTS
from managevcs.nodes import FileNode
from managevcs.utils.compat import unittest
from managevcs.utils.diffs import get_gitdiff

class DiffsTestMixin(BackendTestMixin):

    @classmethod
    def _get_commits(cls):
        commits = [
         {'message': 'Initial commit', 
            'author': 'Joe Doe <joe.doe@example.com>', 
            'date': datetime.datetime(2010, 1, 1, 20), 
            'added': [
                    FileNode('file1', content='Foobar')]},
         {'message': 'Added a file2, change file1', 
            'author': 'Joe Doe <joe.doe@example.com>', 
            'date': datetime.datetime(2010, 1, 1, 20), 
            'added': [
                    FileNode('file2', content='Foobar')], 
            'changed': [
                      FileNode('file1', content='...')]},
         {'message': 'Remove file1', 
            'author': 'Joe Doe <joe.doe@example.com>', 
            'date': datetime.datetime(2010, 1, 1, 20), 
            'removed': [
                      FileNode('file1')]}]
        return commits

    def test_log_command(self):
        commits = [ self.repo.get_changeset(r) for r in self.repo.revisions ]
        commit1, commit2, commit3 = commits
        old = commit1.get_node('file1')
        new = commit2.get_node('file1')
        result = get_gitdiff(old, new).splitlines()
        self.assertEqual(result[0], 'diff --git a/file1 b/file1')
        self.assertIn('-Foobar', result)
        self.assertIn('+...', result)


for alias in SCM_TESTS:
    attrs = {'backend_alias': alias}
    cls_name = ('').join(('%s diff tests' % alias).title().split())
    bases = (DiffsTestMixin, unittest.TestCase)
    globals()[cls_name] = type(cls_name, bases, attrs)

if __name__ == '__main__':
    unittest.main()