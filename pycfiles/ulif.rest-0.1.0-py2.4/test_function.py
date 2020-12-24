# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ulif/rest/tests/test_directives/test_function.py
# Compiled at: 2008-02-24 09:47:58
"""
Tests for the 'function' directive.
"""
from __init__ import DocutilsTestSupport
import directives_plain

def suite():
    s = DocutilsTestSupport.ParserTestSuite()
    s.generateTests(totest)
    return s


totest = {}
totest['function directive'] = [
 [
  '.. function:: myfunction(param1[, param2=None])\n', '<document source="test data">\n    <admonition classes="desc-function" desctype="function">\n        <inline first="False">\n            <strong>\n                myfunction\n            <inline>\n            <inline>\n                (\n                <emphasis>\n                    param1\n                <inline>\n                    [\n                    <inline>\n                        , \n                    <emphasis>\n                        param2=None\n                    <inline>\n                        ]\n            <inline>\n                )\n        <container>\n'], ['.. function:: myfunction()\n\n   The function is applied to this paragraph.\n\n   And this one.\n', '<document source="test data">\n    <admonition classes="desc-function" desctype="function">\n        <inline first="False">\n            <strong>\n                myfunction\n            <inline>\n                ()\n        <container>\n            <paragraph>\n                The function is applied to this paragraph.\n            <paragraph>\n                And this one.\n']]
if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')