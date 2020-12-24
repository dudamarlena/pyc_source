# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/unimr/memcachedlock/tests.py
# Compiled at: 2009-04-16 11:19:33
import unittest
from zope.testing import doctestunit
from zope.component import testing
from Testing import ZopeTestCase as ztc

def test_suite():
    return unittest.TestSuite([doctestunit.DocFileSuite('README.txt', package='unimr.memcachedlock', setUp=testing.setUp, tearDown=testing.tearDown)])


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')