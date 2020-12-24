# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sparrow/tests/test_docs.py
# Compiled at: 2009-07-20 09:57:48
import unittest, doctest, datetime
from StringIO import StringIO
FLAGS = doctest.NORMALIZE_WHITESPACE + doctest.ELLIPSIS
GLOBS = {'StringIO': StringIO}

def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
     doctest.DocFileSuite('README.txt', package='sparrow', globs=GLOBS, optionflags=FLAGS)])
    return suite