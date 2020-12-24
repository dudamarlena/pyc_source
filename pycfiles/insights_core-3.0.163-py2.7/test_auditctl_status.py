# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_auditctl_status.py
# Compiled at: 2019-05-16 13:41:33
from insights.tests import context_wrap
from insights.parsers.auditctl_status import AuditctlStatus
from insights.parsers import ParseException
import pytest
NORMAL_AUDS_RHEL6 = ('\nAUDIT_STATUS: enabled=1 flag=1 pid=1483 rate_limit=0 backlog_limit=8192 lost=3 backlog=0\n').strip()
NORMAL_AUDS_RHEL7 = ('\nenabled 1\nfailure 1\npid 947\nrate_limit 0\nbacklog_limit 320\nlost 0\nbacklog 0\nloginuid_immutable 1 locked\n').strip()
BLANK_INPUT_SAMPLE = ('\n').strip()
BAD_INPUT_SAMPLE = ('\nUnknown: type=0, len=0\n').strip()
BAD_INPUT_MIX = ('\nUnknown: type=0, len=0\nenabled 1\n').strip()

def test_normal_auds_rhel6():
    auds = AuditctlStatus(context_wrap(NORMAL_AUDS_RHEL6))
    assert 'enabled' in auds
    assert 'loginuid_immutable' not in auds
    assert auds['pid'] == 1483


def test_normal_auds_rhel7():
    auds = AuditctlStatus(context_wrap(NORMAL_AUDS_RHEL7))
    assert 'loginuid_immutable' in auds
    assert auds['loginuid_immutable'] == '1 locked'
    assert auds['failure'] == 1
    assert auds.get('nonexists') is None
    return


def test_auds_blank_input():
    ctx = context_wrap(BLANK_INPUT_SAMPLE)
    with pytest.raises(ParseException) as (sc):
        AuditctlStatus(ctx)
    assert 'Input content is empty.' in str(sc)


def test_auds_bad_input():
    auds = AuditctlStatus(context_wrap(BAD_INPUT_SAMPLE))
    assert auds.data == {}


def test_auds_bad_input_mix():
    auds = AuditctlStatus(context_wrap(BAD_INPUT_MIX))
    assert 'enabled' in auds