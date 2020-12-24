# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/onepassword_local_search/services/AccountService_test.py
# Compiled at: 2019-05-24 16:38:48
# Size of source mod 2**32: 1672 bytes
import pytest
import onepassword_local_search.services.ConfigFileService as ConfigFileService
import onepassword_local_search.services.AccountService as AccountService
import onepassword_local_search.services.StorageService as StorageService
from onepassword_local_search.tests.fixtures_common import op_session, op_personal_session, op_dual_session

@pytest.mark.usefixtures('op_session')
def test_available_accounts_team_only():
    accounts = AccountService(StorageService(), ConfigFileService()).accounts
    assert len(accounts) == 1
    assert accounts[0]['shorthand'] == 'onepassword_local_search'


@pytest.mark.usefixtures('op_dual_session')
def test_available_accounts_dual_session():
    accounts = AccountService(StorageService(), ConfigFileService()).accounts
    assert len(accounts) == 2
    shorthands = sorted([accounts[0]['shorthand'], accounts[1]['shorthand']])
    assert shorthands == ['my', 'onepassword_local_search']


@pytest.mark.usefixtures('op_dual_session')
def test_available_vaults_dual_session():
    vaults = AccountService(StorageService(), ConfigFileService()).available_vaults
    assert len(vaults) == 4
    assert sorted([vault['uuid'] for vault in vaults]) == ['jih4mxjnvmpcollannoie5gt4u', 'rloeunbmcvvniz7wedijvqhnhu', 'wbt4wkbfztldfolbdfyo2rnfdu', 'zcud5s5loxyjcaig545zwkxe2i']


@pytest.mark.usefixtures('op_session')
def test_available_vaults_main_session():
    vaults = AccountService(StorageService(), ConfigFileService()).available_vaults
    assert len(vaults) == 3
    assert sorted([vault['uuid'] for vault in vaults]) == ['jih4mxjnvmpcollannoie5gt4u', 'rloeunbmcvvniz7wedijvqhnhu', 'wbt4wkbfztldfolbdfyo2rnfdu']