# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_crypto_policies_config.py
# Compiled at: 2019-05-16 13:41:33
from insights.tests import context_wrap
from insights.parsers.crypto_policies import CryptoPoliciesConfig
from insights.parsers import SkipException
import pytest
CONFIG = ('\nDEFAULT\n').strip()
CONFIG_COMMENTED = ("\n# This file should contain a single keyword, the crypto policy to\n# be applied by default to applications. The available policies are \n# restricted to the following profiles.\n#\n# * LEGACY: Ensures maximum compatibility with legacy systems (64-bit\n#   security)\n#\n# * DEFAULT: A reasonable default for today's standards (112-bit security).\n#\n# * FUTURE: A level that will provide security on a conservative level that is\n#   believed to withstand any near-term future attacks (128-bit security).\n#\n# * FIPS: Policy that enables only FIPS 140-2 approved or allowed algorithms.\n#\n# After modifying this file, you need to run update-crypto-policies\n# for the changes to propagate.\n#\nDEFAULT\n").strip()

def test_crypto_policies_config():
    result = CryptoPoliciesConfig(context_wrap(CONFIG))
    assert result.value == 'DEFAULT'


def test_crypto_policies_commented():
    result = CryptoPoliciesConfig(context_wrap(CONFIG_COMMENTED))
    assert result.value == 'DEFAULT'


def test_crypto_policies_config_empty():
    with pytest.raises(SkipException):
        CryptoPoliciesConfig(context_wrap(''))