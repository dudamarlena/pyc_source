# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ivan/release/sqlitedict/tests/test_onimport.py
# Compiled at: 2017-10-18 05:34:28
"""Test cases for on-import logic."""
import unittest, sys
from accessories import TestCaseBackport

class SqliteDict_cPickleImportTest(TestCaseBackport):
    """Verify fallback to 'pickle' module when 'cPickle' is not found."""

    def setUp(self):
        self.orig_meta_path = sys.meta_path
        self.orig_sqlitedict = orig_sqlitedict = sys.modules.pop('sqlitedict', None)

        class FauxMissingImport(object):

            def __init__(self, *args):
                self.module_names = args

            def find_module(self, fullname, path=None):
                if fullname in self.module_names:
                    return self
                else:
                    return

            def load_module(self, name):
                raise ImportError('No module named %s (FauxMissingImport)' % (name,))

        sys.modules.pop('cPickle', None)
        sys.modules.pop('pickle', None)
        sys.meta_path.insert(0, FauxMissingImport('cPickle'))
        return

    def tearDown(self):
        sys.meta_path = self.orig_meta_path
        if self.orig_sqlitedict:
            sys.modules['sqlitedict'] = self.orig_sqlitedict

    def test_cpickle_fallback_to_pickle(self):
        sqlitedict = __import__('sqlitedict')
        self.assertIn('pickle', sys.modules.keys())
        self.assertIs(sqlitedict.dumps, sys.modules['pickle'].dumps)


class SqliteDictPython24Test(TestCaseBackport):
    """Verify ImportError when using python2.4 or earlier."""

    def setUp(self):
        self._orig_version_info = sys.version_info
        sys.version_info = (2, 4, 0, 'does-not-matter', 0)
        self.orig_sqlitedict = sys.modules.pop('sqlitedict', None)
        return

    def tearDown(self):
        sys.version_info = self._orig_version_info
        if self.orig_sqlitedict:
            sys.modules['sqlitedict'] = self.orig_sqlitedict

    def test_py24_error(self):
        with self.assertRaises(ImportError):
            __import__('sqlitedict')