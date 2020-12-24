# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/docbook2sla/tests/old/testWrapper.py
# Compiled at: 2008-03-14 13:07:50
import os, sys, unittest, tempfile
from docbook2sla import DocBook2Sla

class WrapperTests(unittest.TestCase):
    __module__ = __name__

    def testWrapper(self):
        """ Wrapper should generate an id attribute for every xml node.

            xsltproc -o tests/data/testWrapper.output.expected.xml                      --stringparam secondinput ../tests/data/testWrapper.input.xml                      xsl/wrapper.xsl                      tests/data/testWrapper.input.scribus.xml
        """
        d2s = DocBook2Sla()
        outputfn = d2s.wrapper('tests/data/testWrapper.input.xml', 'tests/data/testWrapper.input.scribus.xml')
        output = open(outputfn, 'r')
        expected_output = open('tests/data/testWrapper.output.expected.xml', 'r')
        self.assertEqual(output.read(), expected_output.read())


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(WrapperTests))
    return suite


if __name__ == '__main__':
    unittest.main()