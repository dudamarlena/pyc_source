# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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