# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/bitwarden_simple_cli/services/CipherService_test.py
# Compiled at: 2019-04-19 09:41:11
# Size of source mod 2**32: 484 bytes
import pytest
import bitwarden_simple_cli.services.CipherService as CipherService
from bitwarden_simple_cli.tests.fixtures_common import bw_session, cipher_service, common_data

@pytest.mark.usefixtures('bw_session')
def test_cipher_service(cipher_service):
    cipher = cipher_service.get(common_data('uuid_login_personal'))
    assert cipher.id == 'fd8870cc-3659-40aa-9492-aa3000cedbb3'
    assert cipher.organizationId is None
    assert cipher.userId == common_data('user_id')