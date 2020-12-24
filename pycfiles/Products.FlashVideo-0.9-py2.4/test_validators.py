# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Products\FlashVideo\tests\test_validators.py
# Compiled at: 2009-03-02 16:14:25
"""
Unit tests for validators
"""
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