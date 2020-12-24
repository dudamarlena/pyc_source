# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/clue/app/tests.py
# Compiled at: 2008-06-27 12:03:50
import unittest, doctest, os, logging

def test_suite():
    flags = doctest.ELLIPSIS
    os.environ['cluemapper.loglevel'] = str(logging.FATAL)
    suite = unittest.TestSuite()
    suite.addTest(doctest.DocTestSuite('clue.app.admin', optionflags=flags))
    suite.addTest(doctest.DocTestSuite('clue.app.config', optionflags=flags))
    suite.addTest(doctest.DocTestSuite('clue.app.controller', optionflags=flags))
    suite.addTest(doctest.DocTestSuite('clue.app.environinit', optionflags=flags))
    suite.addTest(doctest.DocTestSuite('clue.app.patches', optionflags=flags))
    suite.addTest(doctest.DocTestSuite('clue.app.pdbcheck', optionflags=flags))
    suite.addTest(doctest.DocTestSuite('clue.app.project', optionflags=flags))
    suite.addTest(doctest.DocTestSuite('clue.app.redirect', optionflags=flags))
    suite.addTest(doctest.DocTestSuite('clue.app.server', optionflags=flags))
    suite.addTest(doctest.DocTestSuite('clue.app.utils', optionflags=flags))
    suite.addTest(doctest.DocFileSuite('cluemapper.txt', package='clue.app', optionflags=flags))
    return suite


def main():
    runner = unittest.TextTestRunner()
    runner.run(test_suite())


if __name__ == '__main__':
    main()