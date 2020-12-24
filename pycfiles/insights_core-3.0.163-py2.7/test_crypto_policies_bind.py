# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_crypto_policies_bind.py
# Compiled at: 2019-05-16 13:41:33
from insights.tests import context_wrap
from insights.parsers.crypto_policies import CryptoPoliciesBind
from insights.parsers import SkipException
import pytest
CONFIG = ('\ndisable-algorithms "." {\nRSAMD5;\nDSA;\n};\ndisable-ds-digests "." {\nGOST;\n};\n').strip()
CONFIG_EMPTY_SECTIONS = ('\ndisable-algorithms "." {\n};\ndisable-ds-digests "." {\n};\n').strip()

def test_crypto_policies_bind():
    result = CryptoPoliciesBind(context_wrap(CONFIG))
    assert 'GOST' in result.disable_ds_digests
    assert 'DSA' in result.disable_algorithms
    assert ['RSAMD5', 'DSA'] == result.disable_algorithms
    assert ['GOST'] == result.disable_ds_digests


def test_crypto_policies_bind_empty():
    with pytest.raises(SkipException):
        CryptoPoliciesBind(context_wrap(''))
    result = CryptoPoliciesBind(context_wrap(CONFIG_EMPTY_SECTIONS))
    assert [] == result.disable_algorithms
    assert [] == result.disable_ds_digests