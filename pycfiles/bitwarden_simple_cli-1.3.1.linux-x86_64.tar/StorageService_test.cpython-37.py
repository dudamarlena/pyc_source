# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/bitwarden_simple_cli/services/StorageService_test.py
# Compiled at: 2019-04-19 09:41:11
# Size of source mod 2**32: 1161 bytes
import os, pytest
import bitwarden_simple_cli.services.StorageService as StorageService
from bitwarden_simple_cli.tests.fixtures_common import storage_service, common_data

def test_storage_service_init_without_db_path():
    storage_service = StorageService()
    assert os.path.isfile(storage_service.database_path)


@pytest.mark.usefixtures('storage_service')
def test_storage_service_init_without_db_path(storage_service):
    assert os.path.isfile(storage_service.database_path)
    assert os.path.basename(storage_service.database_path) == common_data('test_database_filename')
    assert storage_service.database is not None
    assert storage_service.database.get('userEmail') == common_data('user_email')
    assert storage_service.database.get('userId') == common_data('user_id')
    assert storage_service.database.get('__PROTECTED__key') == common_data('protected_key')
    assert 'ciphers_' + common_data('user_id') in storage_service.database
    assert 'organizations_' + common_data('user_id') in storage_service.database
    assert common_data('organization_id') in storage_service.database[('organizations_' + common_data('user_id'))]