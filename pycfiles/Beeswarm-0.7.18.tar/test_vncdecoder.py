# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/honeynet/beeswarm/beeswarm/shared/tests/test_vncdecoder.py
# Compiled at: 2016-11-12 07:38:04
import unittest
from beeswarm.shared.vnc.decoder import VNCDecoder

class VncDecoderTests(unittest.TestCase):

    def test_combinations(self):
        """Tests different combinations of challenge/response pairs and checks if
           we can find the right password.
        """
        passwords = [
         '1q2w3e4r', 'asdf', '1234', 'beeswarm', 'random']
        challenge = b'\x1f\x9c+\t\x14\x03\xfaj\xde\x97p\xe9e\xca\x08\xff'
        response = b'\xe7\xe2\xe2\xa8\x89T\x87\x8d\xf01\x96\x10\xfe\xb9\xc5\xbb'
        decoder = VNCDecoder(challenge, response, passwords)
        computed_pass = decoder.decode()
        self.assertEquals(computed_pass.startswith('1234'), True)


if __name__ == '__main__':
    unittest.main()