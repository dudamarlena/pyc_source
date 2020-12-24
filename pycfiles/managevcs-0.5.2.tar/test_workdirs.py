# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dzhiltsov/Development/vcslib/managevcs/tests/test_workdirs.py
# Compiled at: 2015-06-08 06:25:02
from __future__ import with_statement
import datetime
from managevcs.nodes import FileNode
from managevcs.utils.compat import unittest
from managevcs.tests.base import BackendTestMixin
from managevcs.tests.conf import SCM_TESTS

class WorkdirTestCaseMixin(BackendTestMixin):

    @classmethod
    def _get_commits(cls):
        commits = [
         {'message': 'Initial commit', 
            'author': 'Joe Doe <joe.doe@example.com>', 
            'date': datetime.datetime(2010, 1, 1, 20), 
            'added': [
                    FileNode('foobar', content='Foobar'),
                    FileNode('foobar2', content='Foobar II'),
                    FileNode('foo/bar/baz', content='baz here!')]},
         {'message': 'Changes...', 
            'author': 'Jane Doe <jane.doe@example.com>', 
            'date': datetime.datetime(2010, 1, 1, 21), 
            'added': [
                    FileNode('some/new.txt', content='news...')], 
            'changed': [
                      FileNode('foobar', 'Foobar I')], 
            'removed': []}]
        return commits

    def test_get_branch_for_default_branch(self):
        self.assertEqual(self.repo.workdir.get_branch(), self.repo.DEFAULT_BRANCH_NAME)

    def test_get_branch_after_adding_one(self):
        self.imc.add(FileNode('docs/index.txt', content='Documentation\n'))
        self.imc.commit(message='New branch: foobar', author='joe', branch='foobar')
        self.assertEqual(self.repo.workdir.get_branch(), self.default_branch)

    def test_get_changeset(self):
        old_head = self.repo.get_changeset()
        self.imc.add(FileNode('docs/index.txt', content='Documentation\n'))
        head = self.imc.commit(message='New branch: foobar', author='joe', branch='foobar')
        self.assertEqual(self.repo.workdir.get_branch(), self.default_branch)
        self.repo.workdir.checkout_branch('foobar')
        self.assertEqual(self.repo.workdir.get_changeset(), head)
        self.repo.workdir.checkout_branch(self.default_branch)
        self.assertEqual(self.repo.workdir.get_changeset(), old_head)

    def test_checkout_branch(self):
        from managevcs.exceptions import BranchDoesNotExistError
        self.assertRaises(BranchDoesNotExistError, self.repo.workdir.checkout_branch, branch='foobranch')
        self.imc.add(FileNode('file1', content='blah'))
        self.imc.commit(message='asd', author='john', branch='foobranch')
        self.repo.workdir.checkout_branch()
        self.assertEqual(self.repo.workdir.get_branch(), self.backend_class.DEFAULT_BRANCH_NAME)
        self.repo.workdir.checkout_branch('foobranch')
        self.assertEqual(self.repo.workdir.get_branch(), 'foobranch')


for alias in SCM_TESTS:
    attrs = {'backend_alias': alias}
    cls_name = ('').join(('%s branch test' % alias).title().split())
    bases = (WorkdirTestCaseMixin, unittest.TestCase)
    globals()[cls_name] = type(cls_name, bases, attrs)

if __name__ == '__main__':
    unittest.main()