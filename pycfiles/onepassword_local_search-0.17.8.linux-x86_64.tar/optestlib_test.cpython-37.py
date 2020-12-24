# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/onepassword_local_search/lib/optestlib_test.py
# Compiled at: 2019-05-24 16:38:48
# Size of source mod 2**32: 906 bytes
import pytest
from onepassword_local_search.lib.optestlib import determine_session_file_path_from_session_key
from onepassword_local_search.tests.fixtures_common import common_data

def test_determine_session_file_path_from_session_key():
    assert determine_session_file_path_from_session_key(common_data('session_key')) == common_data('session_filename')
    assert determine_session_file_path_from_session_key('kYOPcBsWTNQ81pfLvlkRs0ogDmooRvs3YKWgKmwLGFA') == '.-eqI_7WLuKYKW7eMBaSmJpEuVrQ'
    assert determine_session_file_path_from_session_key('peuf3297Q_hmWr8RFHi-jCskxnC_v1fmqYK8VdPVtPQ') == '.hHvZhhoB807qm-E2BuK04C_Q60Q'
    assert determine_session_file_path_from_session_key('7hwQ4p4S7UnebRB3bpcy2br_ktUGyd0aGEtRob4im3M') == '.eaQClbtT1fMTfuNJzPkVGC2DsZI'
    assert determine_session_file_path_from_session_key('15RvkcSJWi1TSYlRX6jc-J5IAoYFa5_26C-V6ncptHs') == '.gLR-shwH24wVDAB5E_LoDYDkfDw'