# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_fcoeadm_i.py
# Compiled at: 2019-11-14 13:57:46
from insights.parsers import fcoeadm_i
from insights.parsers import SkipException, ParseException
from insights.parsers.fcoeadm_i import FcoeadmI
from insights.tests import context_wrap
import pytest, doctest
FCOEADM_I_57810 = ('\n        Description:      NetXtreme II BCM57810 10 Gigabit Ethernet\n        Revision:         10\n        Manufacturer:     Broadcom Corporation\n        Serial Number:    2C44FD8F4418\n        Driver:           bnx2x 1.712.30-0\n        Number of Ports:  1\n\n            Symbolic Name:     bnx2fc (QLogic BCM57810) v2.9.6 over eth8.0-fcoe\n            OS Device Name:    host6\n            Node Name:         0x50060B0000C26237\n            Port Name:         0x50060B0000C26236\n            FabricName:        0x0000000000000000\n            Speed:             Unknown\n            Supported Speed:   1 Gbit, 10 Gbit\n            MaxFrameSize:      2048\n            FC-ID (Port ID):   0xFFFFFFFF\n            State:             Online\n\n            Symbolic Name:     bnx2fc (QLogic BCM57810) v2.9.6 over eth6.0-fcoe\n            OS Device Name:    host7\n            Node Name:         0x50060B0000C26235\n            Port Name:         0x50060B0000C26234\n            FabricName:        0x0000000000000000\n            Speed:             Unknown\n            Supported Speed:   1 Gbit, 10 Gbit\n            MaxFrameSize:      2048\n            FC-ID (Port ID):   0xFFFFFFFF\n            State:             Offline\n').strip()

def test_fcoeadm_i():
    result = FcoeadmI(context_wrap(FCOEADM_I_57810, path='/tmp/fcoeadm_i'))
    assert result.fcoe['Driver'] == 'bnx2x 1.712.30-0'
    assert result.fcoe['Revision'] == '10'
    assert result.fcoe['Manufacturer'] == 'Broadcom Corporation'
    assert result.fcoe['Serial Number'] == '2C44FD8F4418'
    assert result.fcoe['Number of Ports'] == '1'
    assert result.iface_list == ['eth8.0-fcoe', 'eth6.0-fcoe']
    assert result.nic_list == ['eth8', 'eth6']
    assert result.stat_list == ['Online', 'Offline']
    assert result.get_host_from_nic('eth8') == 'host6'
    assert result.get_stat_from_nic('eth8') == 'Online'
    assert result['Driver'] == 'bnx2x 1.712.30-0'
    assert result['Revision'] == '10'
    assert result['Manufacturer'] == 'Broadcom Corporation'
    assert result['Serial Number'] == '2C44FD8F4418'
    assert result['Number of Ports'] == '1'
    with pytest.raises(ValueError) as (sc12):
        result.get_stat_from_nic('abf371294f')
    assert 'is NOT real FCoE port provided' in str(sc12)
    with pytest.raises(ValueError) as (sc12):
        result.get_host_from_nic('97hjh38k')
    assert 'is NOT real FCoE port provided' in str(sc12)


def test_fcoeadm_i_documentation():
    """
    Here we test the examples in the documentation automatically using
    doctest.  We set up an environment which is similar to what a
    rule writer might see - a 'fcoeadm_i' command that has been
    passed in as a parameter to the rule declaration.
    """
    env = {'fi': FcoeadmI(context_wrap(FCOEADM_I_57810))}
    failed, total = doctest.testmod(fcoeadm_i, globs=env)
    assert failed == 0


def test_fcoeadm_i_exp():
    """
    Here test the examples cause expections
    """
    with pytest.raises(SkipException) as (sc):
        FcoeadmI(context_wrap(''))
    assert 'Input content is empty' in str(sc)
    with pytest.raises(ParseException) as (sc):
        FcoeadmI(context_wrap('ERROR'))
    assert 'No useful data parsed in content' in str(sc)