# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/bitwarden_simple_cli/models/response/BaseResponse_test.py
# Compiled at: 2019-04-19 09:41:11
# Size of source mod 2**32: 759 bytes
import pytest
import bitwarden_simple_cli.models.response.BaseResponse as BaseResponse
from bitwarden_simple_cli.tests.fixtures_common import common_data

@pytest.fixture()
def base_response():
    return BaseResponse(common_data('cipher_response'))


def test_base_response_get_response_property_name(base_response: BaseResponse):
    uuid = 'fd8870cc-3659-40aa-9492-aa3000cedbb3'
    assert base_response.get_response_property_name('userId') == common_data('user_id')
    assert base_response.get_response_property_name('UserId') == common_data('user_id')
    assert base_response.get_response_property_name('Id') == uuid
    assert base_response.get_response_property_name('id') == uuid
    assert base_response.get_response_property_name('ID') == uuid