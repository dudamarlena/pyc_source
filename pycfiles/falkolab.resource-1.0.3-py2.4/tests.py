# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/falkolab/resource/tests.py
# Compiled at: 2009-08-21 14:46:18
"""
$Id: tests.py 301 2009-08-21 18:46:18Z falko $
"""
import doctest, unittest
from zope import interface
from falkolab.resource import resourcetypes
from falkolab.resource.interfaces import IResourceFactory
from falkolab.resource import testing

class CustomResource(resourcetypes.FileResource):
    __module__ = __name__


class CustomFileResourceFactory(resourcetypes.FileResourceFactory):
    __module__ = __name__
    interface.implements(IResourceFactory)
    options = {}

    def __call__(self, request):
        resource = CustomResource(self._file, request)
        resource.__Security_checker__ = self._checker
        resource.__name__ = self._name
        return resource


def test_suite():
    return unittest.TestSuite((doctest.DocFileSuite('README.txt', setUp=testing.setUp, tearDown=testing.tearDown, optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS), doctest.DocFileSuite('package/package.txt', setUp=testing.setUp, tearDown=testing.tearDown, optionflags=doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS), doctest.DocTestSuite('falkolab.resource.resourcetypes')))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')