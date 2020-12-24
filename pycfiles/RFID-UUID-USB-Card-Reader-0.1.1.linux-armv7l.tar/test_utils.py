# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pi/Desktop/tests/lib/python2.7/site-packages/uuidreader/test/test_utils.py
# Compiled at: 2017-07-29 01:56:49
import uuidreader.utils as utils, unittest

class TestUtils(unittest.TestCase):

    def test_rfid_code_to_uuid(self):
        input = '1234567890'
        output = utils.rfid_code_to_uuid(input)
        self.assertEqual(output, 'd5cdd08d-bab5-5774-a08d-b6a71722301f')
        input = '9876543210'
        output = utils.rfid_code_to_uuid(input)
        self.assertEqual(output, 'e7208e1b-b667-5f7e-81f8-5f1d9084d4f6')


if __name__ == '__main__':
    unittest.main()