# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tests/test_files.py
# Compiled at: 2007-10-25 10:12:01
import os, unittest, md5, gasp.tests, gasp.testing

class GraphicsTest(unittest.TestCase):

    def __init__(self, moduleFileName, testPath, basePath):
        self.moduleFileName = moduleFileName
        self.basePath = basePath
        self.testPath = testPath
        unittest.TestCase.__init__(self)

    def setUp(self):
        self.counter = 0
        self.basename = self.moduleFileName.split('.')[0]
        gasp.testing.TEST_CASE = self

    def tearDown(self):
        gasp.testing.TEST_CASE = None
        return

    def runTest(self):
        name = self.basename
        __import__('gasp.tests.input.' + name)
        if self.counter == 0:
            return
        for i in xrange(self.counter):
            self.assertSameImage(os.path.join(self.basePath, name + '.%i.png' % i), os.path.join(self.testPath, name + '.%i.png' % i))

    def assertSameImage(self, baseImage, testImage):
        basehash = md5.new(open(baseImage, 'r').read())
        testhash = md5.new(open(testImage, 'r').read())
        if basehash.digest() != testhash.digest():
            self.fail('Images do not match.')


def test_suite():
    suite = unittest.TestSuite()
    inputDir = os.path.join(os.path.dirname(gasp.tests.__file__), 'input')
    outputDir = os.path.join(os.path.dirname(gasp.tests.__file__), 'output')
    expectDir = os.path.join(os.path.dirname(gasp.tests.__file__), 'expected')
    for filename in os.listdir(inputDir):
        if not filename.endswith('.py') or filename.startswith('__init__'):
            continue
        TestCase = type(filename[:-3], (GraphicsTest,), {})
        case = TestCase(filename, outputDir, expectDir)
        suite.addTest(case)

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')