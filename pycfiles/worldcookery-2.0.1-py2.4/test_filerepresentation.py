# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.2-i386/egg/worldcookery/tests/test_filerepresentation.py
# Compiled at: 2006-09-21 05:27:35
import unittest
from doctest import DocFileSuite
import zope.component.testing
from zope.filerepresentation.interfaces import IReadFile, IWriteFile, IFileFactory
from worldcookery.interfaces import IRecipe
from worldcookery.filerepresentation import RecipeReadFile, RecipeWriteFile, RecipeFactory, RecipeDirectoryFactory

def setUp(test):
    zope.component.testing.setUp(test)
    zope.component.provideAdapter(RecipeReadFile)
    zope.component.provideAdapter(RecipeWriteFile)
    zope.component.provideAdapter(RecipeFactory)
    zope.component.provideAdapter(RecipeDirectoryFactory)


def test_suite():
    return unittest.TestSuite((DocFileSuite('filerepresentation.txt', package='worldcookery', setUp=setUp, tearDown=zope.component.testing.tearDown),))


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')