# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\SelfTest\Protocol\test_rfc1751.py
# Compiled at: 2013-03-13 13:15:35
__revision__ = '$Id$'
import binascii, unittest
from Crypto.Util import RFC1751
from Crypto.Util.py3compat import *
test_data = [
 ('EB33F77EE73D4053', 'TIDE ITCH SLOW REIN RULE MOT'),
 ('CCAC2AED591056BE4F90FD441C534766', 'RASH BUSH MILK LOOK BAD BRIM AVID GAFF BAIT ROT POD LOVE'),
 ('EFF81F9BFBC65350920CDD7416DE8009', 'TROD MUTE TAIL WARM CHAR KONG HAAG CITY BORE O TEAL AWL')]

class RFC1751Test_k2e(unittest.TestCase):

    def runTest(self):
        """Check converting keys to English"""
        for key, words in test_data:
            key = binascii.a2b_hex(b(key))
            self.assertEqual(RFC1751.key_to_english(key), words)


class RFC1751Test_e2k(unittest.TestCase):

    def runTest(self):
        """Check converting English strings to keys"""
        for key, words in test_data:
            key = binascii.a2b_hex(b(key))
            self.assertEqual(RFC1751.english_to_key(words), key)


def get_tests(config={}):
    return [
     RFC1751Test_k2e(), RFC1751Test_e2k()]


if __name__ == '__main__':
    unittest.main()