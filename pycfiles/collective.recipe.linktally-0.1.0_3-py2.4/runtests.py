# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/recipe/linktally/runtests.py
# Compiled at: 2007-12-20 08:04:40


def test_suite():
    import unittest, doctest
    return unittest.TestSuite(doctest.DocTestSuite('collective.recipe.linktally', optionflags=doctest.ELLIPSIS))


if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='test_suite', argv=[sys.argv[0]] + args)