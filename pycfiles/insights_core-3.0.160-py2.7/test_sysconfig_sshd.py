# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_sysconfig_sshd.py
# Compiled at: 2019-05-16 13:41:33
from insights.tests import context_wrap
from insights.parsers.sysconfig import SshdSysconfig
SSHD_SYSCONFIG = ('\n# Configuration file for the sshd service.\n\n# The server keys are automatically generated if they are missing.\n# To change the automatic creation, adjust sshd.service options for\n# example using  systemctl enable sshd-keygen@dsa.service  to allow creation\n# of DSA key or  systemctl mask sshd-keygen@rsa.service  to disable RSA key\n# creation.\n\n# System-wide crypto policy:\n# To opt-out, uncomment the following line\n# CRYPTO_POLICY=\nCRYPTO_POLICY=\n').strip()

def test_sysconfig_sshd():
    result = SshdSysconfig(context_wrap(SSHD_SYSCONFIG))
    assert result['CRYPTO_POLICY'] == ''
    assert result.get('CRYPTO_POLICY') == ''
    assert result.get('OPTIONS1') is None
    assert 'OPTIONS1' not in result
    assert 'CRYPTO_POLICY' in result
    return