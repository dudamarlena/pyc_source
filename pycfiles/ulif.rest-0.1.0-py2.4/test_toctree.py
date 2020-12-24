# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ulif/rest/tests/test_directives/test_toctree.py
# Compiled at: 2008-02-24 09:47:58
"""
Tests for the 'toctree' directive.
"""
from __init__ import DocutilsTestSupport
import directives_plain

def suite():
    s = DocutilsTestSupport.ParserTestSuite()
    s.generateTests(totest)
    return s


totest = {}
totest['toctree directive'] = [
 [
  '.. toctree::\n\n   file1.rst\n   file2.rest\n   foo\n', '<document source="test data">\n    <comment includefiles="file1.rst file2.rest foo" maxdepth="-1" xml:space="preserve">\n'], ['.. toctree::\n   :maxdepth: 2\n\n   file1.rst\n   file2.rest\n   foo\n', '<document source="test data">\n    <comment includefiles="file1.rst file2.rest foo" maxdepth="2" xml:space="preserve">\n']]
if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')