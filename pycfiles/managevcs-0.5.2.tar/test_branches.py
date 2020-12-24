# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dzhiltsov/Development/vcslib/managevcs/tests/test_branches.py
# Compiled at: 2015-06-08 06:25:00
from __future__ import with_statement
import datetime, managevcs
from managevcs.utils.compat import unittest
from managevcs.nodes import FileNode
from managevcs.tests.base import BackendTestMixin
from managevcs.tests.conf import SCM_TESTS

class BranchesTestCaseMixin(BackendTestMixin):

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

    def test_simple(self):
        tip = self.repo.get_changeset()
        self.assertEqual(tip.date, datetime.datetime(2010, 1, 1, 21))

    def test_new_branch(self):
        self.assertFalse('foobar' in self.repo.branches)
        self.imc.add(managevcs.nodes.FileNode('docs/index.txt', content='Documentation\n'))
        foobar_tip = self.imc.commit(message='New branch: foobar', author='joe', branch='foobar')
        self.assertTrue('foobar' in self.repo.branches)
        self.assertEqual(foobar_tip.branch, 'foobar')

    def test_new_head(self):
        tip = self.repo.get_changeset()
        self.imc.add(managevcs.nodes.FileNode('docs/index.txt', content='Documentation\n'))
        foobar_tip = self.imc.commit(message='New branch: foobar', author='joe', branch='foobar', parents=[
         tip])
        self.imc.change(managevcs.nodes.FileNode('docs/index.txt', content='Documentation\nand more...\n'))
        newtip = self.imc.commit(message='At default branch', author='joe', branch=foobar_tip.branch, parents=[
         foobar_tip])
        newest_tip = self.imc.commit(message='Merged with %s' % foobar_tip.raw_id, author='joe', branch=self.backend_class.DEFAULT_BRANCH_NAME, parents=[
         newtip, foobar_tip])
        self.assertEqual(newest_tip.branch, self.backend_class.DEFAULT_BRANCH_NAME)

    def test_branch_with_slash_in_name(self):
        self.imc.add(managevcs.nodes.FileNode('extrafile', content='Some data\n'))
        self.imc.commit('Branch with a slash!', author='joe', branch='issue/123')
        self.assertTrue('issue/123' in self.repo.branches)

    def test_branch_with_slash_in_name_and_similar_without(self):
        self.imc.add(managevcs.nodes.FileNode('extrafile', content='Some data\n'))
        self.imc.commit('Branch with a slash!', author='joe', branch='issue/123')
        self.imc.add(managevcs.nodes.FileNode('extrafile II', content='Some data\n'))
        self.imc.commit('Branch without a slash...', author='joe', branch='123')
        self.assertIn('issue/123', self.repo.branches)
        self.assertIn('123', self.repo.branches)


for alias in SCM_TESTS:
    attrs = {'backend_alias': alias}
    cls_name = ('').join(('%s branches test' % alias).title().split())
    bases = (BranchesTestCaseMixin, unittest.TestCase)
    globals()[cls_name] = type(cls_name, bases, attrs)

if __name__ == '__main__':
    unittest.main()