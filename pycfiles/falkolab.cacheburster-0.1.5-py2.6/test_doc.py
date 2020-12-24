# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/falkolab/cacheburster/tests/test_doc.py
# Compiled at: 2010-12-07 03:05:46
import re, os, unittest
from zope.app.testing import functional
from zope.testing import renormalizing
from falkolab.cacheburster.testing import CacheBursterLayer, testsPath
from falkolab.cacheburster.tests.test_directive import request

def getTemplateContent(name):
    pageTemplate = os.path.join(os.path.dirname(__file__), 'testfiles', name)
    f = open(pageTemplate, 'r')
    data = f.read()
    f.close()
    return data


def test_suite():
    suite = unittest.TestSuite()
    s = functional.FunctionalDocFileSuite('../README.txt', globs={'getTemplateContent': getTemplateContent, 'testsPath': testsPath, 
       'request': request}, checker=renormalizing.RENormalizing([
     (
      re.compile('httperror_seek_wrapper:', re.M), 'HTTPError:')]))
    s.layer = CacheBursterLayer
    suite.addTest(s)
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')