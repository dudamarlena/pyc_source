# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-ppc/egg/nva/stormcontainer/tests/test_doctests.py
# Compiled at: 2008-01-27 03:34:49
import unittest
from zope.testing import doctest
from storm.locals import *

class Person(object):
    __module__ = __name__
    __storm_table__ = 'person'
    id = Int(primary=True)
    name = Unicode()


def test_suite():
    return unittest.TestSuite((doctest.DocFileSuite('README.txt', package='nva.stormcontainer', optionflags=doctest.ELLIPSIS),))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')