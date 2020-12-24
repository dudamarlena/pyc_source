# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/thevpncompany/test/test_certificate.py
# Compiled at: 2019-07-12 00:27:44
# Size of source mod 2**32: 864 bytes
import unittest
from unittest.mock import patch
import json
from .mock import response
import logging
from ..consumer_openvpn_certificates import process_single_certificate
log = logging.getLogger(__name__)

def mocked_vpnapi_save_certificate(*args, **kwargs):
    return response.MockResponse({'response': 0}, 200)


class TestCertificates(unittest.TestCase):

    @patch('requests.put', side_effect=mocked_vpnapi_save_certificate)
    def test_create_server(self, mock_post):
        """
        Test the creation of a server
        """
        import random
        request = json.loads('{"common_name": "random@email.com' + str(random.randint(1, 10000)) + '"}')
        result = process_single_certificate(request)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()