# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/lukasz/develop/workspace/.pythonpath/vcs/tests/test_filenodes_unicode_path.py
# Compiled at: 2013-04-27 15:11:11
from __future__ import with_statement
import datetime
from vcs.nodes import FileNode
from vcs.utils.compat import unittest
from vcs.tests.test_inmemchangesets import BackendBaseTestCase
from vcs.tests.conf import SCM_TESTS

class FileNodeUnicodePathTestsMixin(object):
    fname = 'ąśðąęłąć.txt'
    ufname = fname.decode('utf-8')

    def get_commits(self):
        self.nodes = [
         FileNode(self.fname, content='Foobar')]
        commits = [
         {'message': 'Initial commit', 
            'author': 'Joe Doe <joe.doe@example.com>', 
            'date': datetime.datetime(2010, 1, 1, 20), 
            'added': self.nodes}]
        return commits

    def test_filenode_path(self):
        node = self.tip.get_node(self.fname)
        unode = self.tip.get_node(self.ufname)
        self.assertEqual(node, unode)


for alias in SCM_TESTS:
    attrs = {'backend_alias': alias}
    cls_name = ('').join(('%s file node unicode path test' % alias).title().split())
    bases = (
     FileNodeUnicodePathTestsMixin, BackendBaseTestCase)
    globals()[cls_name] = type(cls_name, bases, attrs)

if __name__ == '__main__':
    unittest.main()