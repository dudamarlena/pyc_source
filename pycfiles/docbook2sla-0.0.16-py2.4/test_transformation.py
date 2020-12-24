# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/docbook2sla/tests/test_transformation.py
# Compiled at: 2008-03-27 15:37:39
import os, sys, unittest, tempfile
from lxml import etree
from StringIO import StringIO
from docbook2sla import DocBook2Sla
dirname = os.path.dirname(__file__)

class TransformationTestCase(unittest.TestCase):
    __module__ = __name__

    def setUp(self):
        self.d2s = DocBook2Sla()

    def testTransformation(self):
        """ Test transformation function. """
        inputfn = os.path.join(os.path.dirname(__file__), 'data', 'test_transformation', 'testTransformation.input.xml')
        transformfn = os.path.join(os.path.dirname(__file__), 'data', 'test_transformation', 'testTransformation.xsl')
        expectedfn = os.path.join(os.path.dirname(__file__), 'data', 'test_transformation', 'testTransformation.expected.xml')
        try:
            outputfn = self.d2s.transform(inputfn, transformfn)
        except:
            print >> sys.stderr, 'Error transforming %s with %s' % (inputfn, transformfn)
            raise

        output = open(outputfn, 'r')
        expected = open(expectedfn, 'r')
        self.assertEqual(output.read(), expected.read())
        return outputfn

    def testTransformationWithParam(self):
        """ Test transformation function (with params). """
        inputfn = os.path.join(os.path.dirname(__file__), 'data', 'test_transformation', 'testTransformationWithParam.input.xml')
        secondinputfn = os.path.join(os.path.dirname(__file__), 'data', 'test_transformation', 'testTransformationWithParam.secondinput.xml')
        transformfn = os.path.join(os.path.dirname(__file__), 'data', 'test_transformation', 'testTransformationWithParam.xsl')
        expectedfn = os.path.join(os.path.dirname(__file__), 'data', 'test_transformation', 'testTransformationWithParam.expected.xml')
        try:
            outputfn = self.d2s.transform(inputfn, transformfn, secondinputfn=secondinputfn)
        except:
            print >> sys.stderr, 'Error transforming %s with %s' % (inputfn, transformfn)
            raise

        output = open(outputfn, 'r').read()
        expected = open(expectedfn, 'r').read()
        self.assertEqual(output, expected)
        return outputfn


def test_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(TransformationTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
    return suite


if __name__ == '__main__':
    test_suite()