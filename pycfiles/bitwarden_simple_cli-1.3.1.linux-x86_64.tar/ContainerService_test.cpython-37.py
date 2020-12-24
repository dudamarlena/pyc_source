# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/bitwarden_simple_cli/services/ContainerService_test.py
# Compiled at: 2019-04-19 09:41:11
# Size of source mod 2**32: 1127 bytes
import pytest
import bitwarden_simple_cli.services.ContainerService as ContainerService
import bitwarden_simple_cli.services.StorageService as StorageService
import bitwarden_simple_cli.services.SecureStorageService as SecureStorageService
import bitwarden_simple_cli.services.CryptoService as CryptoService
from bitwarden_simple_cli.tests.fixtures_common import bw_session

@pytest.mark.usefixtures('bw_session')
def test_container_service():
    storage_service = StorageService()
    crypto_service = CryptoService(storage_service)
    secure_storage_service = SecureStorageService(storage_service, crypto_service)
    container_service = ContainerService()
    container_service.add_service(crypto_service)
    container_service.add_service(secure_storage_service)
    container_service2 = ContainerService()
    assert container_service.get_crypto_service() == crypto_service
    assert container_service.get_secure_storage_service() == secure_storage_service
    assert container_service2.get_crypto_service() == crypto_service
    assert container_service2.get_secure_storage_service() == secure_storage_service