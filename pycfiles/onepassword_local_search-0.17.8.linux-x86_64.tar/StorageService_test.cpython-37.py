# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/onepassword_local_search/services/StorageService_test.py
# Compiled at: 2019-05-24 16:38:48
# Size of source mod 2**32: 844 bytes
import pytest
from onepassword_local_search.tests.fixtures_common import storage_service, common_data

def test_item_query(storage_service):
    enc_item = storage_service.get_item_by_uuid(common_data('item_uuid'))
    assert enc_item['uuid'] == common_data('item_uuid')


def test_item_query_auto_1password(storage_service):
    enc_item = storage_service.get_item_by_uuid(common_data('login_uuid'))
    assert enc_item['uuid'] == common_data('login_uuid')


def test_item_query_auto_lastpass(storage_service):
    enc_item = storage_service.get_item_by_uuid(common_data('login_lastpass_uuid'))
    assert enc_item['uuid'] == common_data('login_uuid')


def test_item_query_auto_custom(storage_service):
    enc_item = storage_service.get_item_by_uuid(common_data('login_custom_uuid'))
    assert enc_item['uuid'] == common_data('login_uuid')