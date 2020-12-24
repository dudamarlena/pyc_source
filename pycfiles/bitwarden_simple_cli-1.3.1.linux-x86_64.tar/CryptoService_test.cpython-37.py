# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/bitwarden_simple_cli/services/CryptoService_test.py
# Compiled at: 2019-04-19 09:41:11
# Size of source mod 2**32: 1262 bytes
import pytest
import bitwarden_simple_cli.services.CryptoService as CryptoService
import bitwarden_simple_cli.models.domain.SymmetricCryptoKey as SymmetricCryptoKey
from bitwarden_simple_cli.tests.fixtures_common import bw_session, crypto_service
import bitwarden_simple_cli.services.ContainerService as ContainerService
import bitwarden_simple_cli.services.SecureStorageService as SecureStorageService

@pytest.mark.usefixtures('bw_session')
def test_has_key(crypto_service: CryptoService):
    ContainerService().add_service(SecureStorageService(crypto_service.storageService, crypto_service))
    assert crypto_service.has_key() == True


@pytest.mark.usefixtures('bw_session')
def test_get_key(crypto_service: CryptoService):
    ContainerService().add_service(SecureStorageService(crypto_service.storageService, crypto_service))
    key = crypto_service.get_key()
    assert key is not None
    assert isinstance(key, SymmetricCryptoKey)
    assert key.encType.value == 0
    assert key.keyB64 == b'/lCGAMDGAq+mjRP3FJv+VNDDnbrYcVGnsiPeXTm4NfU='
    assert key.encKeyB64 == b'/lCGAMDGAq+mjRP3FJv+VNDDnbrYcVGnsiPeXTm4NfU='