# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.freebsd-7.1-PRERELEASE-i386/egg/Products/XMLWidgets/tests/test_all.py
# Compiled at: 2008-08-28 08:23:26
import unittest
try:
    import Zope2
except ImportError:
    import Zope as Zope2

try:
    startup = Zope2.startup
except (AttributeError, ImportError):
    pass
else:
    startup()

from Products.XMLWidgets.tests import test_EditorService
from Products.XMLWidgets.tests import test_EditorCache

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(test_EditorService.test_suite())
    suite.addTest(test_EditorCache.test_suite())
    return suite


def main():
    unittest.TextTestRunner(verbosity=1).run(test_suite())


if __name__ == '__main__':
    main()