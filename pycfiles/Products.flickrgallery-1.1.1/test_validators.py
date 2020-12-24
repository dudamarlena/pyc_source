# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\Products\FlashVideo\tests\test_validators.py
# Compiled at: 2009-03-02 16:14:25
__doc__ = '\nUnit tests for validators\n'
import unittest, sys, os
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
from Products.FlashVideo.validators import FLVValidator
from BaseTest import FakeFile

class FLVValidatorTests(unittest.TestCase):
    """
    Test class for FLVValidator class
    """
    __module__ = __name__

    def _readFile(self, name='test_movie.flv', data=None):
        """
        """
        if not data:
            ihome = os.environ.get('INSTANCE_HOME')
            path = os.path.join(ihome, 'Products', 'FlashVideo', 'tests', name)
            data = file(path, 'r').read()
        fakefile = FakeFile()
        fakefile.write(data)
        fakefile.seek(0)
        return fakefile

    def test_init(self):
        """
        Simple class instance
        """
        validator = FLVValidator('isFLVFile')
        self.assertEqual(getattr(validator, 'name', ''), 'isFLVFile')

    def test__call__good(self):
        """
        Test __call__ method with correct file
        """
        validator = FLVValidator('isFLVFile')
        flv_file = self._readFile()
        result = validator.__call__(flv_file)
        self.assertEqual(result, 1)

    def test__call__bad(self):
        """
        Test __call__ method with incorrect file
        """
        validator = FLVValidator('isFLVFile')
        flv_file = self._readFile(name='test_movie.jpg')
        result = validator.__call__(flv_file)
        self.assertEqual(result, 'This does not appear to be an FLV file')
        flv_file2 = self._readFile(data='FLV1234')
        result = validator.__call__(flv_file2)
        self.assertEqual(result, 'Data size too small')


def test_suite():
    """
    Build test suite
    """
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(sys.modules[__name__])
    return suite


def main():
    """
    Run tests
    """
    unittest.TextTestRunner().run(test_suite())


if __name__ == '__main__':
    main()