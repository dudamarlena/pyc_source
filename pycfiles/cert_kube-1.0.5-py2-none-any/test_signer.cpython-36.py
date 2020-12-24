# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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