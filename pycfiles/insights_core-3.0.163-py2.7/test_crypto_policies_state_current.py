# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_crypto_policies_state_current.py
# Compiled at: 2019-05-16 13:41:33
from insights.tests import context_wrap
from insights.parsers.crypto_policies import CryptoPoliciesStateCurrent
from insights.parsers import SkipException
import pytest
CONFIG = ('\nDEFAULT\n').strip()

def test_crypto_policies_state_current():
    result = CryptoPoliciesStateCurrent(context_wrap(CONFIG))
    assert result.value == 'DEFAULT'


def test_crypto_policies_state_current_empty():
    with pytest.raises(SkipException):
        CryptoPoliciesStateCurrent(context_wrap(''))