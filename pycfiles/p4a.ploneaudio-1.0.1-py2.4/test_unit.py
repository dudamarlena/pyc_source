# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/p4a/ploneaudio/tests/test_unit.py
# Compiled at: 2007-11-27 08:53:02
import doctest, unittest
from zope.testing import doctestunit
from zope.component import testing

def test_suite():
    suite = unittest.TestSuite()
    if __name__ not in ('__main__', 'p4a.ploneaudio.tests.test_unit'):
        return suite
    suite.addTest(doctestunit.DocTestSuite('p4a.ploneaudio'))
    suite.addTest(doctestunit.DocTestSuite('p4a.ploneaudio.content'))
    suite.addTest(doctestunit.DocFileSuite('atct.txt', package='p4a.ploneaudio', optionflags=doctest.ELLIPSIS, setUp=testing.setUp, tearDown=testing.tearDown))
    suite.addTest(doctestunit.DocFileSuite('indexing.txt', package='p4a.ploneaudio', optionflags=doctest.ELLIPSIS))
    suite.addTest(doctestunit.DocFileSuite('sitesetup.txt', package='p4a.ploneaudio', optionflags=doctest.ELLIPSIS))
    suite.addTest(doctestunit.DocFileSuite('syndication.txt', package='p4a.ploneaudio', optionflags=doctest.ELLIPSIS))
    return suite