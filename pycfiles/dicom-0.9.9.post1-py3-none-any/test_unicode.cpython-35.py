# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\git\pydicom-clean\source\build\lib\dicom\test\test_unicode.py
# Compiled at: 2017-01-26 21:10:19
# Size of source mod 2**32: 567 bytes
import dicom, unittest

class UnicodeFilenames(unittest.TestCase):

    def testRead(self):
        """Unicode: Can read a file with unicode characters in name................"""
        uni_name = 'test°'
        try:
            dicom.read_file(uni_name)
        except UnicodeEncodeError:
            self.fail('UnicodeEncodeError generated for unicode name')
        except IOError:
            pass


if __name__ == '__main__':
    unittest.main()