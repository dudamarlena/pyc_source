# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_signer.py
# Compiled at: 2019-06-10 10:01:36
# Size of source mod 2**32: 363 bytes
import unittest, mock
from cert_issuer.signer import FinalizableSigner

class TestSigner(unittest.TestCase):

    def test_finalizable_signer(self):
        mock_sm = mock.Mock()
        with FinalizableSigner(mock_sm) as (fs):
            mock_sm.start.assert_called()
        mock_sm.stop.assert_called()


if __name__ == '__main__':
    unittest.main()