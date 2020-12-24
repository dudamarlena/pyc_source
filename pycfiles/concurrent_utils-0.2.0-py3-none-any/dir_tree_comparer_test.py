# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/concurrent_tree_crawler/common/test/dir_tree_comparer_test.py
# Compiled at: 2011-09-28 13:52:18
import unittest, os.path
from concurrent_tree_crawler.common.dir_tree_comparer import are_dir_trees_equal
from concurrent_tree_crawler.common.resources import Resources

class DirTreeComparerTestCase(unittest.TestCase):

    def test_equal_dir_trees(self):
        self.__check('equal_dir_trees', True)

    def test_additional_dir(self):
        self.__check('additional_dir', False)

    def test_additional_file(self):
        self.__check('additional_file', False)

    def test_missing_dir(self):
        self.__check('missing_dir', False)

    def test_missing_file(self):
        self.__check('missing_file', False)

    def test_one_byte_different_in_one_file(self):
        self.__check('one_byte_different_in_one_file', False)

    def __check(self, dir_name, should_be_equal):
        path = Resources.path(__file__, os.path.join('data/dir_tree_comparer', dir_name))
        ret = are_dir_trees_equal(os.path.join(path, '01'), os.path.join(path, '02'), ignore=['.gitignore'])
        if should_be_equal:
            self.assertTrue(ret)
        else:
            self.assertFalse(ret)