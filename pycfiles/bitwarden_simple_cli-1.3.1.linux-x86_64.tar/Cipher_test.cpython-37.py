# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/bitwarden_simple_cli/models/domain/Cipher_test.py
# Compiled at: 2019-04-19 09:41:11
# Size of source mod 2**32: 1123 bytes
import pytest
import bitwarden_simple_cli.models.domain.Cipher as Cipher
import bitwarden_simple_cli.services.StorageService as StorageService
from bitwarden_simple_cli.tests.fixtures_common import common_data, storage_service
from bitwarden_simple_cli.services.CipherService import Keys
import bitwarden_simple_cli.models.domain.Login as Login
import bitwarden_simple_cli.enums.CipherType as CipherType

@pytest.fixture()
def cipher_login_personal(storage_service: StorageService):
    cipher_response = storage_service.get(Keys['ciphersPrefix'] + common_data('user_id'))[common_data('uuid_login_personal')]
    return Cipher(cipher_response)


def test_cipher_login_personal(cipher_login_personal: Cipher):
    assert cipher_login_personal.id == 'fd8870cc-3659-40aa-9492-aa3000cedbb3'
    assert cipher_login_personal.organizationId is None
    assert cipher_login_personal.type == CipherType.Login
    assert isinstance(cipher_login_personal.login, Login)
    assert type(cipher_login_personal.fields).__name__ == 'list'
    assert len(cipher_login_personal.fields) == 4