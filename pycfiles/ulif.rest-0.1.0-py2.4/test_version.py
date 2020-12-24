# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ulif/rest/tests/test_directives/test_version.py
# Compiled at: 2008-02-24 09:47:58
"""
Tests for the 'version' directive.

Includes test for ``deprecated``, ``versionadded`` and
``versionchanged``.
"""
from __init__ import DocutilsTestSupport
import directives_plain

def suite():
    s = DocutilsTestSupport.ParserTestSuite()
    s.generateTests(totest)
    return s


totest = {}
totest['version directives'] = [
 [
  '.. deprecated::\n', '<document source="test data">\n    <system_message level="3" line="1" source="test data" type="ERROR">\n        <paragraph>\n            Error in "deprecated" directive:\n            1 argument(s) required, 0 supplied.\n        <literal_block xml:space="preserve">\n            .. deprecated::\n'], ['.. deprecated:: foo\n', '<document source="test data">\n    <system_message level="3" line="1" source="test data" type="ERROR">\n        <paragraph>\n            The "deprecated" admonition is empty; content required.\n        <literal_block xml:space="preserve">\n            .. deprecated:: foo\n'], ['.. deprecated:: 1.0a\n\n   The data is applied to this paragraph.\n\n   And this one.\n', '<document source="test data">\n    <admonition classes="deprecated">\n        <title>\n            Deprecated from version 1.0a: \n        <paragraph>\n            The data is applied to this paragraph.\n        <paragraph>\n            And this one.\n']]
if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')