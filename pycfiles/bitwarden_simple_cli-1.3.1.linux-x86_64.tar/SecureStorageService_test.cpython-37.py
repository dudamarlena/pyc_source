# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/bitwarden_simple_cli/services/SecureStorageService_test.py
# Compiled at: 2019-04-19 09:41:11
# Size of source mod 2**32: 373 bytes
import pytest
from bitwarden_simple_cli.tests.fixtures_common import common_data, secure_storage_service, bw_session

@pytest.mark.usefixtures('bw_session')
def test_secure_storage_service_get(secure_storage_service):
    assert secure_storage_service.get('userId') is None
    assert secure_storage_service.get('key') == b'/lCGAMDGAq+mjRP3FJv+VNDDnbrYcVGnsiPeXTm4NfU='