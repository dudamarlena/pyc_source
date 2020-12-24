# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/docbook2sla/tests/old/testConversion.py
# Compiled at: 2008-03-14 13:07:50
import os, sys, unittest
from zope.interface.verify import verifyClass
import tempfile
from docbook2sla.interfaces import IDocBook2Sla
from docbook2sla.docbook2sla import DocBook2Sla
docbook1 = os.path.join(os.path.dirname(__file__), 'data', 'docbook1.xml')
scribus1 = os.path.join(os.path.dirname(__file__), 'data', 'scribus1.sla')
transform = os.path.join(os.path.dirname(__file__), 'data', 'merge.xsl')
expected_result = os.path.join(os.path.dirname(__file__), 'data', 'expected_result.sla')

class ConverterTests(unittest.TestCase):
    __module__ = __name__

    def testInterfaces(self):
        verifyClass(IDocBook2Sla, DocBook2Sla)


class RegressionTests(unittest.TestCase):
    __module__ = __name__

    def testConversion(self):
        print >> sys.stderr, 'Param: %s, %s, %s' % (docbook1, scribus1, transform)
        try:
            output_filename = DocBook2Sla().convert(docbook1, scribus1, transform, 'output1.sla')
        except:
            print >> sys.stderr, 'Error converting %s and %s with %s' % (docbook1, scribus1, transform)
            raise

        datei = open(output_filename, 'r')
        zeilen = []
        while 1:
            zeile = datei.readline()
            if zeile == '':
                break
            zeilen.append(zeile)

        datei.close()
        print >> sys.stderr, 'Output: %s' % zeilen

    def testSimplePageobject(self):
        """
        """
        pass


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(ConverterTests))
    suite.addTest(makeSuite(RegressionTests))
    return suite


if __name__ == '__main__':
    unittest.main()