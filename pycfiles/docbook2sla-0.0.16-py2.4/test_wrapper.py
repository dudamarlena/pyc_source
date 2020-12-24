# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/docbook2sla/tests/test_wrapper.py
# Compiled at: 2008-03-14 13:07:50
import os, sys, unittest, tempfile
from lxml import etree
from StringIO import StringIO
from docbook2sla import DocBook2Sla
dirname = os.path.dirname(__file__)

class WrapperTestCase(unittest.TestCase):
    """ Test the wrapper stylesheet """
    __module__ = __name__

    def setUp(self):
        self.d2s = DocBook2Sla()
        self.xsl_wrapper = os.path.abspath(os.path.join(dirname, '..', 'xsl', 'wrapper.xsl'))
        if not os.path.exists(self.xsl_wrapper):
            raise IOError('%s does not exist' % self.xsl_wrapper)
        self.scribus_wrapper = os.path.abspath(os.path.join(dirname, 'data', 'test_wrapper_input.xml'))
        self.pageobjects = os.path.abspath(os.path.join(dirname, 'data', 'test_wrapper_secondinput.xml'))
        self.expectedfn = os.path.abspath(os.path.join(dirname, 'data', 'test_wrapper_expected.xml'))
        self.expected = open(self.expectedfn, 'r').read()
        self.outputfn = self.d2s.transform(self.scribus_wrapper, self.xsl_wrapper, secondinputfn=self.pageobjects)
        self.output = open(self.outputfn, 'r').read()

    def testOutput(self):
        """ Test output """
        pass


def test_suite():
    suite = unittest.TestLoader().loadTestsFromTestCase(WrapperTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
    return suite


if __name__ == '__main__':
    test_suite()