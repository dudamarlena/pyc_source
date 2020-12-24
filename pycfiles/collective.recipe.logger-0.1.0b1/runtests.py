# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/recipe/linktally/runtests.py
# Compiled at: 2007-12-20 08:04:40


def test_suite():
    import unittest, doctest
    return unittest.TestSuite(doctest.DocTestSuite('collective.recipe.linktally', optionflags=doctest.ELLIPSIS))


if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='test_suite', argv=[sys.argv[0]] + args)