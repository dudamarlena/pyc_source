# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dusanklinec/workspace/py-trezor-crypto/trezor_crypto_tests/test.py
# Compiled at: 2018-05-23 06:53:41
import unittest, binascii, logging
logger = logging.getLogger(__name__)
from trezor_crypto import trezor_cfunc
tcry = trezor_cfunc

class TcryTest(unittest.TestCase):
    """Simple tests"""

    def __init__(self, *args, **kwargs):
        super(TcryTest, self).__init__(*args, **kwargs)

    def setUp(self):
        trezor_cfunc.open_lib()

    def test_ed_crypto(self):
        h_hex = '8b655970153799af2aeadc9ff1add0ea6c7251d54154cfa92c173a0dd39c1f94'
        h = binascii.unhexlify(h_hex)
        pt = tcry.ge25519_unpack_vartime_r(tcry.KEY_BUFF(*bytes(h)))
        packed = tcry.ge25519_pack_r(pt)


if __name__ == '__main__':
    unittest.main()