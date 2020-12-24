# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tests/services/test_base.py
# Compiled at: 2020-02-03 17:04:46
# Size of source mod 2**32: 1020 bytes
from unittest import TestCase
from unittest.mock import patch
from casper.services.ec2 import EC2Service
from casper.services.base import get_service, UnsupportedServiceException, SUPPORTED_SERVICES

class TestBaseService(TestCase):

    def setUp(self) -> None:
        self.ec2 = EC2Service()

    @patch('logging.Logger.debug')
    def test_get_cloud_resources_unsupported_group(self, logger):
        test_group = 'unsupported_group'
        handler = self.ec2.get_cloud_resources(group=test_group)
        logger.assert_called_once()
        logger.assert_called_with(f"Service Handler for {test_group} is not currently supported")
        self.assertIsNone(handler)

    def test_get_unsupported_service(self):
        service_name = 'unsupported_service'
        self.assertRaises(UnsupportedServiceException, get_service, service_name)

    def test_get_all_supported_service(self):
        for svc in SUPPORTED_SERVICES:
            self.assertIsNotNone(get_service(svc))