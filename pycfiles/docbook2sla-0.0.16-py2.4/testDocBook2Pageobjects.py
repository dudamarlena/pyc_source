# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/docbook2sla/tests/old/testDocBook2Pageobjects.py
# Compiled at: 2008-03-14 13:07:50
import os, sys, unittest, tempfile
from docbook2sla import DocBook2Sla

class DocBook2PageobjectsTests(unittest.TestCase):
    __module__ = __name__

    def testDocBook2Pageobjects(self):
        """ . """
        d2s = DocBook2Sla()
        outputfn = d2s.docbook2Pageobjects('tests/data/testDocBook2Pageobjects.input.xml')
        output = open(outputfn, 'r')
        expected_output = open('tests/data/testDocBook2Pageobjects.output.expected.xml', 'r')
        self.assertEqual(output.read(), expected_output.read())


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(DocBook2PageobjectsTests))
    return suite


if __name__ == '__main__':
    unittest.main()