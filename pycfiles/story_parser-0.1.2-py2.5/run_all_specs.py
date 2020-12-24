# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/story_parser/specs/run_all_specs.py
# Compiled at: 2009-09-25 12:01:44
from parsing_invalid_stories import *
from parsing_valid_stories import *
from story_parser import parser
import regex_with_i18n, doctest
MODULES_WITH_DOCTESTS = (
 regex_with_i18n, parser)
if __name__ == '__main__':
    suite = unittest.TestSuite()
    for obj in globals().values():
        if unittest.TestCase in getattr(obj, '__bases__', []):
            suite.addTest(unittest.makeSuite(obj))

    for module in MODULES_WITH_DOCTESTS:
        suite.addTest(doctest.DocTestSuite(module))

    runner = unittest.TextTestRunner(verbosity=1)
    runner.run(suite)