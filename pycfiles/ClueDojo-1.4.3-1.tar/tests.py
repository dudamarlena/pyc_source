# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/cluebin/tests.py
# Compiled at: 2008-06-27 12:04:19
import unittest, doctest

def test_suite():
    flags = doctest.ELLIPSIS
    suite = unittest.TestSuite()
    suite.addTest(doctest.DocTestSuite('cluebin.paste', optionflags=flags))
    suite.addTest(doctest.DocTestSuite('cluebin.pastebin', optionflags=flags))
    suite.addTest(doctest.DocTestSuite('cluebin.utils', optionflags=flags))
    return suite


def main():
    runner = unittest.TextTestRunner()
    runner.run(test_suite())


if __name__ == '__main__':
    main()