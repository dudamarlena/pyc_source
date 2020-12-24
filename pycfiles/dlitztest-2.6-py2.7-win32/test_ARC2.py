# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\SelfTest\Cipher\test_ARC2.py
# Compiled at: 2013-03-13 13:15:35
"""Self-test suite for Crypto.Cipher.ARC2"""
__revision__ = '$Id$'
from common import dict
import unittest
from Crypto.Util.py3compat import *
test_data = [
 (
  '0000000000000000', 'ebb773f993278eff', '0000000000000000',
  'RFC2268-1', dict(effective_keylen=63)),
 (
  'ffffffffffffffff', '278b27e42e2f0d49', 'ffffffffffffffff',
  'RFC2268-2', dict(effective_keylen=64)),
 (
  '1000000000000001', '30649edf9be7d2c2', '3000000000000000',
  'RFC2268-3', dict(effective_keylen=64)),
 (
  '0000000000000000', '61a8a244adacccf0', '88',
  'RFC2268-4', dict(effective_keylen=64)),
 (
  '0000000000000000', '6ccf4308974c267f', '88bca90e90875a',
  'RFC2268-5', dict(effective_keylen=64)),
 (
  '0000000000000000', '1a807d272bbe5db1', '88bca90e90875a7f0f79c384627bafb2',
  'RFC2268-6', dict(effective_keylen=64)),
 (
  '0000000000000000', '2269552ab0f85ca6', '88bca90e90875a7f0f79c384627bafb2',
  'RFC2268-7', dict(effective_keylen=128)),
 (
  '0000000000000000', '5b78d3a43dfff1f1',
  '88bca90e90875a7f0f79c384627bafb216f80a6f85920584c42fceb0be255daf1e',
  'RFC2268-8', dict(effective_keylen=129)),
 ('0000000000000000', '624fb3e887419e48', '5068696c6970476c617373', 'PCTv201-0'),
 ('ffffffffffffffff', '79cadef44c4a5a85', '5068696c6970476c617373', 'PCTv201-1'),
 ('0001020304050607', '90411525b34e4c2c', '5068696c6970476c617373', 'PCTv201-2'),
 ('0011223344556677', '078656aaba61cbfb', '5068696c6970476c617373', 'PCTv201-3'),
 ('0000000000000000', 'd7bcc5dbb4d6e56a', 'ffffffffffffffff', 'PCTv201-4'),
 ('ffffffffffffffff', '7259018ec557b357', 'ffffffffffffffff', 'PCTv201-5'),
 ('0001020304050607', '93d20a497f2ccb62', 'ffffffffffffffff', 'PCTv201-6'),
 ('0011223344556677', 'cb15a7f819c0014d', 'ffffffffffffffff', 'PCTv201-7'),
 ('0000000000000000', '63ac98cdf3843a7a', 'ffffffffffffffff5065746572477265656e6177617953e5ffe553',
 'PCTv201-8'),
 ('ffffffffffffffff', '3fb49e2fa12371dd', 'ffffffffffffffff5065746572477265656e6177617953e5ffe553',
 'PCTv201-9'),
 ('0001020304050607', '46414781ab387d5f', 'ffffffffffffffff5065746572477265656e6177617953e5ffe553',
 'PCTv201-10'),
 ('0011223344556677', 'be09dc81feaca271', 'ffffffffffffffff5065746572477265656e6177617953e5ffe553',
 'PCTv201-11'),
 ('0000000000000000', 'e64221e608be30ab', '53e5ffe553', 'PCTv201-12'),
 ('ffffffffffffffff', '862bc60fdcd4d9a9', '53e5ffe553', 'PCTv201-13'),
 ('0001020304050607', '6a34da50fa5e47de', '53e5ffe553', 'PCTv201-14'),
 ('0011223344556677', '584644c34503122c', '53e5ffe553', 'PCTv201-15')]

class BufferOverflowTest(unittest.TestCase):

    def setUp(self):
        global ARC2
        from Crypto.Cipher import ARC2

    def runTest(self):
        """ARC2 with keylength > 128"""
        key = 'x' * 16384
        mode = ARC2.MODE_ECB
        self.assertRaises(ValueError, ARC2.new, key, mode)


def get_tests(config={}):
    from Crypto.Cipher import ARC2
    from common import make_block_tests
    tests = make_block_tests(ARC2, 'ARC2', test_data)
    tests.append(BufferOverflowTest())
    return tests


if __name__ == '__main__':
    import unittest
    suite = lambda : unittest.TestSuite(get_tests())
    unittest.main(defaultTest='suite')