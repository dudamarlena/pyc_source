# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Crypto\SelfTest\Hash\test_HMAC.py
# Compiled at: 2013-03-14 04:43:25
"""Self-test suite for Crypto.Hash.HMAC"""
__revision__ = '$Id$'
from common import dict
from Crypto.Util.py3compat import *
test_data = [
 (
  '0b' * 16,
  '4869205468657265',
  dict(default='9294727a3638bb1c13f48ef8158bfc9d'),
  'default-is-MD5'),
 (
  '0b' * 16,
  '4869205468657265',
  dict(MD5='9294727a3638bb1c13f48ef8158bfc9d'),
  'RFC 2202 #1-MD5 (HMAC-MD5)'),
 (
  '0b' * 20,
  '4869205468657265',
  dict(SHA1='b617318655057264e28bc0b6fb378c8ef146be00'),
  'RFC 2202 #1-SHA1 (HMAC-SHA1)'),
 (
  '4a656665',
  '7768617420646f2079612077616e7420666f72206e6f7468696e673f',
  dict(MD5='750c783e6ab0b503eaa86e310a5db738', SHA1='effcdf6ae5eb2fa2d27416d5f184df9c259a7c79'),
  'RFC 2202 #2 (HMAC-MD5/SHA1)'),
 (
  'aa' * 16,
  'dd' * 50,
  dict(MD5='56be34521d144c88dbb8c733f0e8b3f6'),
  'RFC 2202 #3-MD5 (HMAC-MD5)'),
 (
  'aa' * 20,
  'dd' * 50,
  dict(SHA1='125d7342b9ac11cd91a39af48aa17b4f63f175d3'),
  'RFC 2202 #3-SHA1 (HMAC-SHA1)'),
 (
  '0102030405060708090a0b0c0d0e0f10111213141516171819',
  'cd' * 50,
  dict(MD5='697eaf0aca3a3aea3a75164746ffaa79', SHA1='4c9007f4026250c6bc8414f9bf50c86c2d7235da'),
  'RFC 2202 #4 (HMAC-MD5/SHA1)'),
 (
  '0c' * 16,
  '546573742057697468205472756e636174696f6e',
  dict(MD5='56461ef2342edc00f9bab995690efd4c'),
  'RFC 2202 #5-MD5 (HMAC-MD5)'),
 (
  '0c' * 20,
  '546573742057697468205472756e636174696f6e',
  dict(SHA1='4c1a03424b55e07fe7f27be1d58bb9324a9a5a04'),
  'RFC 2202 #5-SHA1 (HMAC-SHA1)'),
 (
  'aa' * 80,
  '54657374205573696e67204c6172676572205468616e20426c6f636b2d53697a' + '65204b6579202d2048617368204b6579204669727374',
  dict(MD5='6b1ab7fe4bd7bf8f0b62e6ce61b9d0cd', SHA1='aa4ae5e15272d00e95705637ce8a3b55ed402112'),
  'RFC 2202 #6 (HMAC-MD5/SHA1)'),
 (
  'aa' * 80,
  '54657374205573696e67204c6172676572205468616e20426c6f636b2d53697a' + '65204b657920616e64204c6172676572205468616e204f6e6520426c6f636b2d' + '53697a652044617461',
  dict(MD5='6f630fad67cda0ee1fb1f562db3aa53e', SHA1='e8e99d0f45237d786d6bbaa7965c7808bbff1a91'),
  'RFC 2202 #7 (HMAC-MD5/SHA1)'),
 (
  '0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b0b',
  '4869205468657265',
  dict(SHA256='\n            b0344c61d8db38535ca8afceaf0bf12b\n            881dc200c9833da726e9376c2e32cff7\n        '),
  'RFC 4231 #1 (HMAC-SHA256)'),
 (
  '4a656665',
  '7768617420646f2079612077616e7420666f72206e6f7468696e673f',
  dict(SHA256='\n            5bdcc146bf60754e6a042426089575c7\n            5a003f089d2739839dec58b964ec3843\n        '),
  'RFC 4231 #2 (HMAC-SHA256)'),
 (
  'aa' * 20,
  'dd' * 50,
  dict(SHA256='\n            773ea91e36800e46854db8ebd09181a7\n            2959098b3ef8c122d9635514ced565fe\n        '),
  'RFC 4231 #3 (HMAC-SHA256)'),
 (
  '0102030405060708090a0b0c0d0e0f10111213141516171819',
  'cd' * 50,
  dict(SHA256='\n            82558a389a443c0ea4cc819899f2083a\n            85f0faa3e578f8077a2e3ff46729665b\n        '),
  'RFC 4231 #4 (HMAC-SHA256)'),
 (
  'aa' * 131,
  '54657374205573696e67204c6172676572205468616e20426c6f636b2d53697a' + '65204b6579202d2048617368204b6579204669727374',
  dict(SHA256='\n            60e431591ee0b67f0d8a26aacbf5b77f\n            8e0bc6213728c5140546040f0ee37f54\n        '),
  'RFC 4231 #6 (HMAC-SHA256)'),
 (
  'aa' * 131,
  '5468697320697320612074657374207573696e672061206c6172676572207468' + '616e20626c6f636b2d73697a65206b657920616e642061206c61726765722074' + '68616e20626c6f636b2d73697a6520646174612e20546865206b6579206e6565' + '647320746f20626520686173686564206265666f7265206265696e6720757365' + '642062792074686520484d414320616c676f726974686d2e',
  dict(SHA256='\n            9b09ffa71b942fcb27635fbcd5b0e944\n            bfdc63644f0713938a7f51535c3a35e2\n        '),
  'RFC 4231 #7 (HMAC-SHA256)')]
hashlib_test_data = [
 (
  '4a656665',
  '7768617420646f2079612077616e74' + '20666f72206e6f7468696e673f',
  dict(SHA224='a30e01098bc6dbbf45690f3a7e9e6d0f8bbea2a39e6148008fd05e44'),
  'RFC 4634 8.4 SHA224 (HMAC-SHA224)'),
 (
  '4a656665',
  '7768617420646f2079612077616e74' + '20666f72206e6f7468696e673f',
  dict(SHA384='af45d2e376484031617f78d2b58a6b1b9c7ef464f5a01b47e42ec3736322445e8e2240ca5e69e2c78b3239ecfab21649'),
  'RFC 4634 8.4 SHA384 (HMAC-SHA384)'),
 (
  '4a656665',
  '7768617420646f2079612077616e74' + '20666f72206e6f7468696e673f',
  dict(SHA512='164b7a7bfcf819e2e395fbe73b56e0a387bd64222e831fd610270cd7ea2505549758bf75c05a994a6d034f65f8f0e6fdcaeab1a34d4a6b4b636e070a38bce737'),
  'RFC 4634 8.4 SHA512 (HMAC-SHA512)')]

def get_tests(config={}):
    global test_data
    from Crypto.Hash import HMAC, MD5, SHA1, SHA256
    from common import make_mac_tests
    hashmods = dict(MD5=MD5, SHA1=SHA1, SHA256=SHA256, default=None)
    try:
        from Crypto.Hash import SHA224, SHA384, SHA512
        hashmods.update(dict(SHA224=SHA224, SHA384=SHA384, SHA512=SHA512))
        test_data += hashlib_test_data
    except ImportError:
        import sys
        sys.stderr.write('SelfTest: warning: not testing HMAC-SHA224/384/512 (not available)\n')

    return make_mac_tests(HMAC, 'HMAC', test_data, hashmods)


if __name__ == '__main__':
    import unittest
    suite = lambda : unittest.TestSuite(get_tests())
    unittest.main(defaultTest='suite')