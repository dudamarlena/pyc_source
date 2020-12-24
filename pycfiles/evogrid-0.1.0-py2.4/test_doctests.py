# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/evogrid/common/tests/test_doctests.py
# Compiled at: 2006-07-12 16:02:04
from zope.testing import doctest
import os.path, unittest
from evogrid.testing import OPTIONS
FILES = (
 os.path.join('..', 'README.txt'), 'test_checkpointers.txt', 'test_elite_archive.txt', 'test_evolvers.txt', 'test_replicators.txt')

def test_suite():
    suite = unittest.TestSuite()
    for filename in FILES:
        suite.addTests(doctest.DocFileSuite(filename, optionflags=OPTIONS))

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')